import { Chat12Regular } from "@fluentui/react-icons";
import styles from "./ChatLoad.module.css";

interface Props {
  onLoad: () => void;
  disabled: boolean;
}

export const ChatLoad = ({ onLoad, disabled }: Props) => {

  const loadChat = () => {
    //if (disabled || chat.length == 0) {
    //return;
    //}
    onLoad();

  };

  const loadChatDisabled = disabled;

  return (
    <div
      role="button"
      tabIndex={0}
      aria-label="Save chat button"
      onClick={loadChat}
      onKeyDown={(e) =>
        e.key === "Enter" || e.key === " " ? loadChat() : null
      }
    >
      <Chat12Regular 
        className={styles.chatIcon} 
        style={{
            background:
                    loadChatDisabled ? "#BDBDBD"
                      : "radial-gradient(109.81% 107.82% at 100.1% 90.19%, #0F6CBD 33.63%, #2D87C3 70.31%, #8DDDD8 100%)",
            cursor: loadChatDisabled ? "" : "pointer",
          }}
        />
    </div>
  );
};
