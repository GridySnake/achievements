import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import FormLogin from "./FormLogin";
import FormSignUp from "./FormSignUp";
import PersonalPageContainer from "./Personal Page/PersonalPageContainer";


const FrontRoutes = () => {
    return (
        <Router>
            <Routes>
                <Route exact path="/signup" element={FormSignUp()}>
                </Route>
                <Route exact path="/login" element={FormLogin()}>
                </Route>
                <Route exact path="/logout">
                </Route>
                <Route exact path="/user/{i}">
                </Route>
                <Route exact path="/subscribes">
                </Route>
                <Route exact path="/chats" key='chats' element={PersonalPageContainer()}>
                </Route>
                <Route path="/chat/">
                </Route>
                <Route exact path="/achievements">
                </Route>
                <Route exact path="/posts">
                </Route>
                <Route exact path="/communities">
                </Route>
                <Route exact path="/courses">
                </Route>
                <Route exact path="/goals">
                </Route>
            </Routes>
        </Router>
)
}

export default FrontRoutes