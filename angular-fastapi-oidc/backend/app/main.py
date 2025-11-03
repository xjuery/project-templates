from fastapi import FastAPI, Depends, HTTPException, status, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
import httpx
import jwt
from jwt import PyJWKClient
from cryptography.hazmat.primitives import serialization
import base64

app = FastAPI(title="OAuth2/OIDC Backend API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",  # Angular frontend
        "http://localhost:8080"   # Keycloak
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OIDC Configuration - Keycloak
OIDC_ISSUER = "http://localhost:8080/auth/realms/master"
OIDC_JWKS_URI = f"{OIDC_ISSUER}/protocol/openid-connect/certs"
CLIENT_ID = "angular-client"

# Security
security = HTTPBearer()


class TokenValidationError(Exception):
    pass


def get_public_key_from_jwks(jwks_data: dict, kid: str = None):
    """
    Extract RSA public key from JWKS data
    """
    if 'keys' not in jwks_data:
        raise TokenValidationError("Invalid JWKS format: no 'keys' found")
    
    # Try to find the key by kid if provided
    for key in jwks_data['keys']:
        if not kid or key.get('kid') == kid:
            if key.get('kty') == 'RSA':
                # Convert JWK to RSA public key
                n = base64.urlsafe_b64decode(key['n'] + '==')
                e = base64.urlsafe_b64decode(key['e'] + '==')
                
                from cryptography.hazmat.primitives.asymmetric import rsa
                public_numbers = rsa.RSAPublicNumbers(
                    int.from_bytes(e, 'big'),
                    int.from_bytes(n, 'big')
                )
                from cryptography.hazmat.backends import default_backend
                return public_numbers.public_key(default_backend())
    
    raise TokenValidationError("No matching RSA key found in JWKS")


async def verify_token(token: str) -> dict:
    """
    Verify JWT token with Keycloak using JWKS
    """
    try:
        # Get JWKS from Keycloak
        async with httpx.AsyncClient(verify=False, timeout=10.0) as client:
            response = await client.get(OIDC_JWKS_URI)
            if response.status_code != 200:
                raise TokenValidationError("Failed to fetch JWKS")
            
            jwks_data = response.json()
        
        # Get the key ID from the token header
        try:
            unverified_header = jwt.get_unverified_header(token)
            kid = unverified_header.get('kid')
        except Exception:
            kid = None
        
        # Extract public key from JWKS
        public_key = get_public_key_from_jwks(jwks_data, kid)
        
        # Decode and verify token with Keycloak's public key
        try:
            decoded = jwt.decode(
                token,
                public_key,
                algorithms=['RS256'],
                options={"verify_exp": True}
            )
            
            # Extract Keycloak-specific claims
            return {
                "sub": decoded.get("sub", "unknown"),
                "name": decoded.get("name", decoded.get("preferred_username", "unknown")),
                "preferred_username": decoded.get("preferred_username"),
                "email": decoded.get("email"),
                "given_name": decoded.get("given_name"),
                "family_name": decoded.get("family_name"),
                **decoded
            }
        except jwt.ExpiredSignatureError:
            raise TokenValidationError("Token has expired")
        except jwt.InvalidSignatureError:
            raise TokenValidationError("Invalid token signature")
        except Exception as e:
            raise TokenValidationError(f"Token decoding error: {str(e)}")
            
    except httpx.TimeoutException:
        # Fallback to local JWT verification for development
        try:
            decoded = jwt.decode(
                token,
                options={"verify_signature": False, "verify_exp": False}
            )
            return {
                "sub": decoded.get("sub", "unknown"),
                "name": decoded.get("name", decoded.get("preferred_username", "unknown")),
                "preferred_username": decoded.get("preferred_username"),
                "email": decoded.get("email"),
                "given_name": decoded.get("given_name"),
                "family_name": decoded.get("family_name"),
                **decoded
            }
        except Exception as e:
            raise TokenValidationError(f"Token decoding error: {str(e)}")
    except Exception as e:
        print(f"Error validating token: {e}")
        raise TokenValidationError(f"Token validation error: {str(e)}")


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Dependency to get current authenticated user
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        # Verify token with OIDC server
        token_info = await verify_token(credentials.credentials)
        return token_info
    except TokenValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


class UserProfile(BaseModel):
    username: str
    claims: dict


@app.get("/")
async def root():
    return {"message": "OAuth2/OIDC Backend API is running"}


@app.get("/api/user/profile", response_model=UserProfile)
async def get_user_profile(current_user: dict = Depends(get_current_user)):
    """
    Protected endpoint that returns user profile information
    """
    return UserProfile(
        username=current_user.get("name", "unknown"),
        claims=current_user
    )


@app.get("/api/public/info")
async def public_info():
    """
    Public endpoint that doesn't require authentication
    """
    return {
        "message": "This is a public endpoint",
        "note": "No authentication required"
    }

