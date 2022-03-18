import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import FormLogin from "./FormLogin";
import FormSignUp from "./FormSignUp";
import PersonalPageContainer from "./Personal Page/PersonalPageContainer";
import SubscribesContainer from "./SubscribesContainer";

// auth? <navbar + all> : <login + signup>
const FrontRoutes = () => {
    return (
        <div>
            <Router>
                <Routes>
                    <Route path="/signup" key="signup" element={<FormSignUp/>}/>
                    <Route path="/login" key="login" element={<FormLogin/>}/>
                    <Route path="/logout" key="logout" />
                    <Route path="/user/:id" key="user:id" element={<PersonalPageContainer/>}/>
                    <Route path="/subscribes" key="subscribes" element={<SubscribesContainer/>}/>
                    <Route path="/chats"/>
                    <Route path="/chat/"/>
                    <Route path="/achievements"/>
                    <Route path="/posts"/>
                    <Route path="/communities"/>
                    <Route path="/courses"/>
                    <Route path="/goals"/>
                </Routes>
            </Router>
        </div>
)
}

export default FrontRoutes