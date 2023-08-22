import { Settings16Regular } from "@fluentui/react-icons";
import styles from "./Settings.module.css";

interface Props {
  onLoad: () => void;
}

export const SettingsButton = ({ onLoad }: Props) => {


const loadSettings = () => {
  onLoad();
};

return (
    <Settings16Regular 
      className={styles.settingsIcon} 
      style={{
          background: "radial-gradient(109.81% 107.82% at 100.1% 90.19%, #0F6CBD 33.63%, #2D87C3 70.31%, #8DDDD8 100%)",
          cursor: "pointer",
        }}
        tabIndex={0}
      aria-label="Settings button"
      onClick={loadSettings}
      onKeyDown={(e) =>
        e.key === "Enter" || e.key === " " ? loadSettings() : null
      }
      />
);
};