import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import FormLogin from "./FormLogin";
import FormSignUp from "./FormSignUp";
import PersonalPageContainer from "./Personal Page/PersonalPageContainer";

const FrontRoutes = () => {
    return (
        <Router>
            <Routes>
                <Route path="/signup" element={<FormSignUp/>}/>
                <Route path="/login" element={<FormLogin/>}/>
                <Route path="/logout"/>
                <Route path="/user/:id" element={<PersonalPageContainer/>}/>
                <Route path="/subscribes"/>
                <Route path="/chats"/>
                <Route path="/chat/"/>
                <Route path="/achievements"/>
                <Route path="/posts"/>
                <Route path="/communities"/>
                <Route path="/courses"/>
                <Route path="/goals"/>
            </Routes>
        </Router>
)
}

export default FrontRoutes