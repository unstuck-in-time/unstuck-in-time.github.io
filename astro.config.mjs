import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";
import mdx from "@astrojs/mdx";
import pagefind from "astro-pagefind";
import tailwindcss from "@tailwindcss/vite";

import react from "@astrojs/react";

// import pdf from "astro-pdf";

// const pdfOptions = {
//   pages: (pathname) => {
//     if (pathname.startsWith("/blog/")) {
//       return {
//         throwOnFail: true,
//         path: pathname.substring(0, pathname.length - 1) + '.pdf',
//         pdf: {
//           displayHeaderFooter: false,
//           outline: true,
//           scale: 0.9,
//           margin: {
//             top: "20mm",
//             bottom: "20mm",
//             left: "15mm",
//             right: "15mm",
//           }
//         }
//       }
//     }
//   }
// }

// https://astro.build/config
export default defineConfig({
  site: "https://unstuck-in-time.github.io",
  integrations: [sitemap(), mdx(), pagefind(), react()], // pdf(pdfOptions)
  vite: {
    plugins: [tailwindcss()],
  },
  markdown: {
    shikiConfig: {
      theme: "css-variables",
    },
  },
});