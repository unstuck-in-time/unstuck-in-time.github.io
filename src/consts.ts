import type { Metadata, Site, Socials } from "@types";

export const SITE: Site = {
  TITLE: "Unstuck In Time",
  DESCRIPTION: "Astro Micro is an accessible and lightweight blog.",
  NUM_POSTS_ON_HOMEPAGE: 5,
  SOURCE: "https://github.com/unstuck-in-time/unstuck-in-time.github.io",
  DEFAULT_IMAGE: "/philosopher.png",
};

export const HOME: Metadata = {
  TITLE: "Home",
  DESCRIPTION: "Astro Micro is an accessible theme for Astro.",
};

export const BLOG: Metadata = {
  TITLE: "Blog",
  DESCRIPTION: "A collection of articles on topics I am passionate about.",
};

export const SOCIALS: Socials = [
  {
    NAME: "Substack",
    HREF: "https://unstuckntime.substack.com",
  },
  {
    NAME: "Medium",
    HREF: "https://medium.com/@unstuck-in-time",
  },
];
