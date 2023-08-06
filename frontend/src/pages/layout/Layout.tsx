import { Outlet, Link } from "react-router-dom";
import styles from "./Layout.module.css";
import { Settings16Filled } from "@fluentui/react-icons";

import { useEffect, useState } from "react";
import { useIsAuthenticated, useMsal } from "@azure/msal-react";
import { SignInButton } from "../../components/Signin/SignInButton";
import { SignOutButton } from "../../components/Signin/SignOutButton";
import { GraphContent } from "../../components/Signin/GraphContent";
import { selectHistoryRequest, ChatMessage } from "../../api";
import { loginRequest } from "../../authConfig";
import { Stack } from "@fluentui/react";

const Layout = (props: any) => {
  const [isSharePanelOpen, setIsSharePanelOpen] = useState<boolean>(false);
  const [copyClicked, setCopyClicked] = useState<boolean>(false);
  const [copyText, setCopyText] = useState<string>("Copy URL");
  const isAuthenticated = useIsAuthenticated();
  const { instance, accounts } = useMsal();

  useEffect(() => {
    if (copyClicked) {
      setCopyText("Copied URL");
    }
  }, [copyClicked]);

  return (
    <div className={styles.layout}>
      <header className={styles.header} role={"banner"}>
        <div className={styles.headerContainer}>
          <Stack horizontal verticalAlign="center">
            <Link to="/" className={styles.headerTitleContainer}>
              <h3 className={styles.headerTitle}>
                Shadow Seller -{" "}
                {isAuthenticated ? <GraphContent /> : "Not logged in"}
              </h3>
            </Link>

            <div className={styles.shareButtonContainer}>
              {isAuthenticated ? <SignOutButton /> : <SignInButton />}
            </div>
          </Stack>
        </div>
      </header>
      <Outlet />
    </div>
  );
};

export default Layout;
