import React from "react";
// import MainTitle from "./components/MainTitle";
// import MainContainer from "./components/MainContainer";
import "./index.css";
import FormLogin from "./components/FormLogin";
// import PersonalPage from "./components/Personal Page/PersonalPageContainer";
import FrontRoutes from "./components/FrontRoutes";
import {AuthWrapper} from "./hooks/AuthHooks";
// import { BrowserRouter } from "react-router-dom";
// import {useAuth} from "./hooks/AuthHooks";
// import Backdrop from '@mui/material/Backdrop';
// import CircularProgress from '@mui/material/CircularProgress';

function App() {
    // const {user, authLoading} = useAuth();

  return (
    <div style={{background: "#F1EDFE"}}>
        {/*{user ?*/}
        <AuthWrapper>
            <FrontRoutes/>
        </AuthWrapper>
            {/*:*/}
            {/*<FormLogin/>*/}
        {/*}*/}
      {/*  <Backdrop*/}
      {/*  sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }}*/}
      {/*  open={authLoading}*/}
      {/*>*/}
      {/*  <CircularProgress color="inherit" />*/}
      {/*</Backdrop>*/}
    </div>
  );
}

export default App;
