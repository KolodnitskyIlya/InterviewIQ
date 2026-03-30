export interface SettingsPreference {
  id: string;
  icon: string;
  label: string;
  enabled: boolean;
}

export interface SettingsLinkItem {
  id: string;
  icon: string;
  label: string;
  value?: string;
  danger?: boolean;
}
