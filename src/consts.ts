import type { Metadata, Site, Socials } from "@types";

export const SITE: Site = {
  TITLE: "Unstuck In Time",
  DESCRIPTION: "Essays in philosophy and cognitive science where I overthink, argue with myself, and probably embarrass myself.",
  NUM_POSTS_ON_HOMEPAGE: 5,
  SOURCE: "https://github.com/unstuck-in-time/unstuck-in-time.github.io",
  DEFAULT_IMAGE: "/philosopher.png",
};

export const HOME: Metadata = {
  TITLE: "Home",
  DESCRIPTION: SITE.DESCRIPTION,
};

export const BLOG: Metadata = {
  TITLE: "Blog",
  DESCRIPTION: SITE.DESCRIPTION,
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
