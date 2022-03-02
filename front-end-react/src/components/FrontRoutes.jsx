import { BrowserRouter as Router, Routes, Route, useParams } from 'react-router-dom';
import FormLogin from "./FormLogin";
import FormSignUp from "./FormSignUp";
import PersonalPageContainer from "./Personal Page/PersonalPageContainer";

// const {id} = useParams()

const FrontRoutes = () => {
    return (
        <Router>
            <Routes>
                <Route path="/signup" element={FormSignUp()}>
                </Route>
                <Route path="/login" element={FormLogin()}>
                </Route>
                <Route path="/logout">
                </Route>
                <Route path="/user/:id">
                </Route>
                <Route path="/subscribes">
                </Route>
                <Route path="/chats" key='chats' element={PersonalPageContainer()}>
                </Route>
                <Route path="/chat/">
                </Route>
                <Route path="/achievements">
                </Route>
                <Route path="/posts">
                </Route>
                <Route path="/communities">
                </Route>
                <Route path="/courses">
                </Route>
                <Route path="/goals">
                </Route>
            </Routes>
        </Router>
)
}

export default FrontRoutes