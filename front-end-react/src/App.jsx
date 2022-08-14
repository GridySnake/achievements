import React, {useContext} from "react";
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
import {useAuth, authContext} from "./hooks/AuthHooks";
import NavbarContainer from "./components/NavbarContainer";
import FooterContainer from "./components/FooterContainer";

function App() {

    const {user} = useAuth();
    console.log(user)
    return (
        <div style={{background: "#F1EDFE"}}>
            {user ?
                <>
                    <NavbarContainer {...user}/>
                    <FrontRoutes {...user}/>
                    <FooterContainer/>
                </>
                :
                <>
                    <NavbarContainer {...user} style={{marginTop: 10}} />
                    <FormLogin/>
                    <FooterContainer/>
                </>
            }
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
