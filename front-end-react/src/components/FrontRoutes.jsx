import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import FormLogin from "./FormLogin";
import FormSignUp from "./FormSignUp";
import PersonalPageContainer from "./Personal Page/PersonalPageContainer";
import SubscribesContainer from "./Subscribes/SubscribesContainer";
import CommunitiesContainer from "./Communities/CommunitiesContainer";
import ChatsContainer from "./Chats/ChatsContainer";
import ChatContainer from "./Chats/ChatContainer";
import UserSettings from "./Personal Page/UserSettings";
import AchievementsContainer from "./Achievements/AchievementsContainer";
import AchievementContainer from "./Achievements/AchievementContainer";
import CoursesContainer from "./Courses/CoursesContainer";
import CourseContainer from "./Courses/CourseContainer";
import CourseContentTableContainer from "./Courses/CourseContentTableContainer";
import CourseContentTaskContainer from "./Courses/CourseContentTaskContainer";
import CourseContentCreateContainer from "./Courses/CourseContentCreateContainer";

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
                    <Route path="/chats" key="chats" element={<ChatsContainer/>}/>
                    <Route path="/chat/:id" key="chat:id" element={<ChatContainer/>}/>
                    <Route path="/achievements" key="achievements" element={<AchievementsContainer/>}/>
                    <Route path="/achievement/:id" key="achievement:id" element={<AchievementContainer/>}/>
                    <Route path="/user_settings" key="user_settings" element={<UserSettings/>}/>
                    <Route path="/feed"/>
                    <Route path="/communities" key="communities" element={<CommunitiesContainer/>}/>
                    <Route path="/courses" key="courses" element={<CoursesContainer/>}/>
                    <Route path="/course/:id" key="course:id" element={<CourseContainer/>}/>
                    <Route path="/study_course/:id" key="study_course:id" element={<CourseContentTableContainer/>}/>
                    <Route path="/study_course/:id/task/:task_id" key="study_course:id_task:task_id" element={<CourseContentTaskContainer/>}/>
                    <Route path="/course/:id/edit_content" key="_course_:id_edit_content" element={<CourseContentCreateContainer/>}/>
                    <Route path="/goals"/>
                </Routes>
            </Router>
        </div>
)
}

export default FrontRoutes