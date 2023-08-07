import { Save16Regular } from "@fluentui/react-icons";
import styles from "./SaveInput.module.css";

interface Props {
  onSave: () => void;
  disabled: boolean;
}

export const SaveInput = ({ onSave, disabled }: Props) => {

  const saveChat = () => {
    //if (disabled || chat.length == 0) {
    //return;
    //}
    onSave();

  };

  const saveChatDisabled = disabled;

  return (
    <div
      role="button"
      tabIndex={0}
      aria-label="Save chat button"
      onClick={saveChat}
      onKeyDown={(e) =>
        e.key === "Enter" || e.key === " " ? saveChat() : null
      }
    >
      <Save16Regular 
        className={styles.saveIcon} 
        style={{
            background:
                    saveChatDisabled ? "#BDBDBD"
                      : "radial-gradient(109.81% 107.82% at 100.1% 90.19%, #0F6CBD 33.63%, #2D87C3 70.31%, #8DDDD8 100%)",
            cursor: saveChatDisabled ? "" : "pointer",
          }}
        />
    </div>
  );
};
