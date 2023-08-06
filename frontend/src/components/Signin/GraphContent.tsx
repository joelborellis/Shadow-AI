import { useState } from "react";
import { useMsal } from "@azure/msal-react";
import { callMsGraph } from '../../graph';
import { loginRequest } from '../../authConfig';
import { ProfileData } from './ProfileData'


export const GraphContent = () =>  {
  const { instance, accounts } = useMsal();
  const [graphData, setGraphData] = useState(null);

    // Silently acquires an access token which is then attached to a request for MS Graph data
    instance
    .acquireTokenSilent({
        ...loginRequest,
        account: accounts[0],
    })
    .then((response) => {
        callMsGraph(response.accessToken).then((response) => setGraphData(response));
    });

  return (
    <>
        {graphData ? (
                <ProfileData graphData={graphData} />
            ) : (
                "No graph data"
            )}
    </>
);
};