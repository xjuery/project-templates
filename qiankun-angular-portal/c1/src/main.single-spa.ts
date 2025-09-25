import 'zone.js';
import { enableProdMode, NgZone } from '@angular/core';
import { bootstrapApplication } from '@angular/platform-browser';
import { Router, NavigationStart } from '@angular/router';
import { singleSpaAngular, getSingleSpaExtraProviders } from 'single-spa-angular';

import { App } from './app/app';
import { appConfig } from './app/app.config';

const lifecycles = singleSpaAngular({
  bootstrapFunction: () => {
    return bootstrapApplication(App, {
      providers: [...getSingleSpaExtraProviders(), ...(appConfig.providers ?? [])],
    });
  },
  template: '<app-root />',
  Router,
  NavigationStart,
  NgZone,
});

export const bootstrap = lifecycles.bootstrap;
export const mount = lifecycles.mount;
export const unmount = lifecycles.unmount;
