import { registerMicroApps, start, loadMicroApp, type MicroApp } from 'qiankun';

const container = document.getElementById('mfe-container');

let app: MicroApp | null = null;

// Register route-based microapps (optional example). We will also allow manual load via sidebar link.
registerMicroApps([
  {
    name: 'mfe-ui',
    entry: 'http://localhost:4200/',
    container: '#mfe-container',
    activeRule: (location) => location.hash.startsWith('#/mfe'),
    props: { portal: 'Qiankun Portal' },
  },
  {
    name: 'c1',
    entry: 'http://localhost:4201/',
    container: '#mfe-container',
    activeRule: (location) => location.hash.startsWith('#/mfe'),
    props: { portal: 'Qiankun Portal' },
  },
]);

start({ prefetch: false, sandbox: { experimentalStyleIsolation: true } });

const link = document.getElementById('load-mfe-link');
if (link && container) {
  link.addEventListener('click', async (e) => {
    e.preventDefault();
    if (app) app.unmount();
    app = await loadMicroApp({
      name: 'mfe-ui-manual',
      entry: 'http://localhost:4200/',
      container,
      props: { portal: 'Qiankun Portal' },
    });
  });
}

const link2 = document.getElementById('load-c1-link');
if (link2 && container) {
    //alert("test1");
  link2.addEventListener('click', async (e) => {
      //alert("test2");
    e.preventDefault();
    //if (app) return;
    if (app) app.unmount();
    app = await loadMicroApp({
      name: 'c1-manual',
      entry: 'http://localhost:4201/',
      container,
      props: { portal: 'Qiankun Portal' },
    });
  });
}
