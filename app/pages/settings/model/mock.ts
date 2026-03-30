import type { SettingsLinkItem } from "@/entities/settings";

export const legalLinks: SettingsLinkItem[] = [
  { id: "privacy", icon: "🛡", label: "Privacy Policy" },
  { id: "terms", icon: "🛡", label: "Terms of Service" },
];

export const accountLinks: SettingsLinkItem[] = [
  { id: "delete", icon: "🗑", label: "Delete Account", danger: true },
];
