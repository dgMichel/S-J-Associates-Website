// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import vercel from '@astrojs/vercel';

const SITE_URL = process.env.PUBLIC_SITE_URL || 'https://www.5j-associates.com';

// https://astro.build/config
export default defineConfig({
  output: 'static',
  adapter: vercel(),
  site: SITE_URL,
  integrations: [
    sitemap({
      changefreq: 'weekly',
      priority: 0.7,
      lastmod: new Date(),
      serialize(item) {
        if (item.url.endsWith('/admin') || item.url.includes('/admin/')) {
          return null;
        }
        if (/\/cars\/[^/]+/.test(item.url)) {
          return {
            ...item,
            changefreq: 'weekly',
            priority: 0.8,
          };
        }
        if (item.url === SITE_URL.replace(/\/$/, '') || item.url === SITE_URL || item.url === SITE_URL + '/') {
          return {
            ...item,
            changefreq: 'daily',
            priority: 1.0,
          };
        }
        return item;
      },
    }),
  ],
});
