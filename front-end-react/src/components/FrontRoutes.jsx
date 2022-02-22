import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import FormLogin from "./FormLogin";

const FrontRoutes = () => {
    return (
        <Router>
            <Routes>
                <Route exact path="/signup">
                </Route>
                <Route exact path="/login" element={FormLogin()}>
                </Route>
                <Route exact path="/logout">
                </Route>
                <Route exact path="/user/{i}">
                </Route>
                <Route exact path="/subscribes">
                </Route>
                <Route exact path="/chats">
                </Route>
                <Route exact path="/chat/{i}">
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