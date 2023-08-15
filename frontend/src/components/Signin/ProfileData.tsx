/**
 * Renders information about the user obtained from MS Graph 
 * @param props
 * 
 *   {props.graphData.givenName};
 *   {props.graphData.surname}
 *   {props.graphData.userPrincipalName}
 */

export const ProfileData = (props: any) => {
  return (
    <>
    {props.graphData.userPrincipalName}
    </>
  );
};