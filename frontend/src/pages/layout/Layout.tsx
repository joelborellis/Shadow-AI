import { Outlet, Link } from "react-router-dom";
import styles from "./Layout.module.css";
import { useState } from "react";

import { useIsAuthenticated, useMsal } from "@azure/msal-react";
import { SignInButton } from "../../components/Signin/SignInButton";
import { SignOutButton } from "../../components/Signin/SignOutButton";
import { SettingsButton } from "../../components/Settings/SettingsButton";
import { GraphContent } from "../../components/Signin/GraphContent";
import { Panel, Stack } from "@fluentui/react";
import { Checkbox, CheckboxProps, Divider, Label } from "@fluentui/react-components";

const Layout = (props: any) => {
  const isAuthenticated = useIsAuthenticated();
  const [isSettingsOpen, setIsSettingsOpen] = useState<boolean>(false);
  const [checked, setChecked] = useState<CheckboxProps["checked"]>(true);

  const dismissSettings = async () => {
    alert(checked);
    setIsSettingsOpen(false);
  };

  const openSettings = async () => {
    setIsSettingsOpen(true);
  };

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
