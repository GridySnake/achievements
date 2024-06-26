import React from "react";
import {useLocation} from "react-router-dom";
import {Menu} from "antd";
import styles from "./css/PersonalPage.module.css";
import StaticFrontPng from './StaticRoutes'
import { Helmet } from "react-helmet";

const NavbarContainer = (user) => {

    const StaticFront = StaticFrontPng.StaticFrontPng
    const {pathname} = useLocation();
    const initials = user.initials
    console.log(pathname)

    const LeftBarLinks = ['/chats', '/subscribes', '/communities', '/feed']

    const LeftBarValues = [
            {'link': '/chats', 'value': 'Messages', 'color': '#8A8A8A', 'className': styles.messagesDiv},
            {'link': '/subscribes', 'value': 'Subscribes', 'color': '#8A8A8A', 'className': styles.friendsDiv},
            {'link': '/communities', 'value': 'Communities', 'color': '#8A8A8A', 'className': styles.communitiesDiv},
            {'link': '/feed', 'value': 'Feed', 'color': '#8A8A8A', 'className': styles.feedDiv}
        ]

    const page = LeftBarLinks.indexOf(pathname)

    const AchievementsPNG = () => {
        if (pathname === '/achievements') {
            return StaticFront + "achievements_active.png"
        } else {
            return StaticFront + "achievements_default.png"
        }
    }

    const GoalsPNG = () => {
        if (pathname === '/goals') {
            return StaticFront + "goals_active.png"
        } else {
            return StaticFront + "goals_default.png"
        }
    }

    const leftBarEllipseV = [styles.ellipseIcon3, styles.ellipseIcon4, styles.ellipseIcon5, styles.ellipseIcon6]

    const LeftBarEllipseStyleFunc = () => {
        const LeftBarEllipseStyle = [false, false, false, false]
        if (page === -1) {
            return LeftBarEllipseStyle
        } else {
            LeftBarEllipseStyle.splice(page, 1, true)
            return LeftBarEllipseStyle
        }
    }
    const leftBarEllipseS = LeftBarEllipseStyleFunc()

    console.log(initials)
    return (
        initials && user?
            // <Menu>
            <div className={styles.personalPageDiv}>
                <Helmet>
                    <meta name="viewport" content="width=device-width, initial-scale=1"/>
                </Helmet>
                <div className={styles.logoDiv}>
                    <div className={styles.aCHIDiv}><a href={`/user/${user.user_id}`}><img src={StaticFront + 'logo.png'}/></a></div>
                </div>
                <div className={styles.leftBarDiv}>
                    <div className={styles.rectangleDiv1} />
                    {LeftBarValues.map((leftBar, index) => {
                        if (page === index) {
                            return (<div className={leftBar.className}><a href={leftBar.link}
                                                                          style={{color: '#F76D7D'}}>{leftBar.value}</a>
                            </div>)
                        } else {
                            return (<div className={leftBar.className}><a href={leftBar.link}
                                                                          style={{color: leftBar.color}}>{leftBar.value}</a>
                                </div>)
                        }
                    })
                    }
                    {leftBarEllipseV.map((ellipse, index) => {
                        if (leftBarEllipseS[index] === true) {
                            return (<img className={ellipse} src={StaticFront + 'ellipse_active.png'}/>)
                        }
                    })}
                    {/*<img className={styles.ellipseIcon3} alt="" />*/}
                    {/*<img className={styles.ellipseIcon4} alt="" />*/}
                    {/*<img className={styles.ellipseIcon5} alt="" />*/}
                    {/*<img className={styles.ellipseIcon6} alt="" />*/}
                </div>
                <div className={styles.rightBarDiv}>
                    <div className={styles.rectangleDiv1} />
                    {pathname === '/courses' ?
                        <div className={styles.coursesDiv}><a href={"/courses"} style={{color: '#F76D7D'}}>Courses</a></div>
                        :
                        <div className={styles.coursesDiv}><a href={"/courses"} style={{color: '#8A8A8A'}}>Courses</a></div>
                    }
                    <a href={"/achievements"}><img className={styles.groupIcon1} src={AchievementsPNG()} /></a>
                    <a href={"/goals"}><img className={styles.groupIcon2} src={GoalsPNG()}/></a>
                    {pathname === '/courses' ?
                        <img className={styles.ellipseIcon7} src={StaticFront + 'ellipse_active.png'}/>
                        :
                        <></>
                    }
                    <img className={styles.ellipseIcon8} src={StaticFront + "ellipse_name.png"} />
                    <b className={styles.lMB}>
                        <span className={styles.lMTxtSpan}>
                            <span>{initials[0]}</span>
                            <span className={styles.mSpan}>{initials[1]}</span>
                        </span>
                    </b>
                </div>
            </div>

            //     <a href={`/user/${user.user_id}`} style={{marginRight: 10}}>Home</a>
            //     <a href={"/chats"} style={{marginRight: 10}}>Messages</a>
            //     <a href={"/subscribes"} style={{marginRight: 10}}>Subscribes</a>
            //     <a href={"/communities"} style={{marginRight: 600}}>Communities</a>
            //
            //     <div name='Rectangle 20'>
            //     <a href={"/achievements"} style={{marginRight: 10}}>
            //         <front_png width="27" height="28" viewBox="0 0 27 28" fill="none" xmlns="http://www.w3.org/2000/svg">
            //         <path d="M13.1804 18C17.8748 18 21.6804 14.1944 21.6804 9.5C21.6804 4.80558 17.8748 1 13.1804 1C8.486 1 4.68042 4.80558 4.68042 9.5C4.68042 14.1944 8.486 18 13.1804 18Z" stroke="#989898" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            //         <path d="M13.1833 18.0043L18 26.3484L20.2639 21.7684L25.361 22.097L20.5444 13.7543" stroke="#989898" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            //         <path d="M5.81667 13.7543L1 22.0984L6.09717 21.7684L8.361 26.347L13.1777 18.0043" stroke="#989898" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            //         </front_png>
            //     </a>
            //     <a href={"/goals"} style={{marginRight: 10}}>
            //         <front_png width="28" height="28" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
            //         <path d="M14 27C21.1797 27 27 21.1797 27 14C27 6.8203 21.1797 1 14 1C6.8203 1 1 6.8203 1 14C1 21.1797 6.8203 27 14 27Z" stroke="#989898" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            //         <path d="M13.9996 15.4445C14.7974 15.4445 15.4441 14.7978 15.4441 14C15.4441 13.2023 14.7974 12.5556 13.9996 12.5556C13.2019 12.5556 12.5552 13.2023 12.5552 14C12.5552 14.7978 13.2019 15.4445 13.9996 15.4445Z" stroke="#989898" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            //         <path d="M16.0366 11.9633L19.7777 8.22223" stroke="#989898" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            //         <path d="M6.77783 14C6.77783 12.0845 7.53874 10.2475 8.89317 8.89311C10.2476 7.53868 12.0846 6.77777 14.0001 6.77777" stroke="#989898" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            //         </front_png>
            //     </a>
            //     <a href={"/courses"} style={{marginRight: 10}}>
            //         <front_png width="87" height="19" viewBox="0 0 87 19" fill="none" xmlns="http://www.w3.org/2000/svg">
            //         <path d="M11.2812 12.5742H13.5312C13.4141 13.6523 13.1055 14.6172 12.6055 15.4688C12.1055 16.3203 11.3984 16.9961 10.4844 17.4961C9.57031 17.9883 8.42969 18.2344 7.0625 18.2344C6.0625 18.2344 5.15234 18.0469 4.33203 17.6719C3.51953 17.2969 2.82031 16.7656 2.23438 16.0781C1.64844 15.3828 1.19531 14.5508 0.875 13.582C0.5625 12.6055 0.40625 11.5195 0.40625 10.3242V8.625C0.40625 7.42969 0.5625 6.34766 0.875 5.37891C1.19531 4.40234 1.65234 3.56641 2.24609 2.87109C2.84766 2.17578 3.57031 1.64062 4.41406 1.26562C5.25781 0.890625 6.20703 0.703125 7.26172 0.703125C8.55078 0.703125 9.64062 0.945313 10.5312 1.42969C11.4219 1.91406 12.1133 2.58594 12.6055 3.44531C13.1055 4.29688 13.4141 5.28516 13.5312 6.41016H11.2812C11.1719 5.61328 10.9688 4.92969 10.6719 4.35938C10.375 3.78125 9.95312 3.33594 9.40625 3.02344C8.85938 2.71094 8.14453 2.55469 7.26172 2.55469C6.50391 2.55469 5.83594 2.69922 5.25781 2.98828C4.6875 3.27734 4.20703 3.6875 3.81641 4.21875C3.43359 4.75 3.14453 5.38672 2.94922 6.12891C2.75391 6.87109 2.65625 7.69531 2.65625 8.60156V10.3242C2.65625 11.1602 2.74219 11.9453 2.91406 12.6797C3.09375 13.4141 3.36328 14.0586 3.72266 14.6133C4.08203 15.168 4.53906 15.6055 5.09375 15.9258C5.64844 16.2383 6.30469 16.3945 7.0625 16.3945C8.02344 16.3945 8.78906 16.2422 9.35938 15.9375C9.92969 15.6328 10.3594 15.1953 10.6484 14.625C10.9453 14.0547 11.1562 13.3711 11.2812 12.5742ZM15.7109 11.8008V11.5312C15.7109 10.6172 15.8438 9.76953 16.1094 8.98828C16.375 8.19922 16.7578 7.51562 17.2578 6.9375C17.7578 6.35156 18.3633 5.89844 19.0742 5.57812C19.7852 5.25 20.582 5.08594 21.4648 5.08594C22.3555 5.08594 23.1562 5.25 23.8672 5.57812C24.5859 5.89844 25.1953 6.35156 25.6953 6.9375C26.2031 7.51562 26.5898 8.19922 26.8555 8.98828C27.1211 9.76953 27.2539 10.6172 27.2539 11.5312V11.8008C27.2539 12.7148 27.1211 13.5625 26.8555 14.3438C26.5898 15.125 26.2031 15.8086 25.6953 16.3945C25.1953 16.9727 24.5898 17.4258 23.8789 17.7539C23.1758 18.0742 22.3789 18.2344 21.4883 18.2344C20.5977 18.2344 19.7969 18.0742 19.0859 17.7539C18.375 17.4258 17.7656 16.9727 17.2578 16.3945C16.7578 15.8086 16.375 15.125 16.1094 14.3438C15.8438 13.5625 15.7109 12.7148 15.7109 11.8008ZM17.8789 11.5312V11.8008C17.8789 12.4336 17.9531 13.0312 18.1016 13.5938C18.25 14.1484 18.4727 14.6406 18.7695 15.0703C19.0742 15.5 19.4531 15.8398 19.9062 16.0898C20.3594 16.332 20.8867 16.4531 21.4883 16.4531C22.082 16.4531 22.6016 16.332 23.0469 16.0898C23.5 15.8398 23.875 15.5 24.1719 15.0703C24.4688 14.6406 24.6914 14.1484 24.8398 13.5938C24.9961 13.0312 25.0742 12.4336 25.0742 11.8008V11.5312C25.0742 10.9062 24.9961 10.3164 24.8398 9.76172C24.6914 9.19922 24.4648 8.70312 24.1602 8.27344C23.8633 7.83594 23.4883 7.49219 23.0352 7.24219C22.5898 6.99219 22.0664 6.86719 21.4648 6.86719C20.8711 6.86719 20.3477 6.99219 19.8945 7.24219C19.4492 7.49219 19.0742 7.83594 18.7695 8.27344C18.4727 8.70312 18.25 9.19922 18.1016 9.76172C17.9531 10.3164 17.8789 10.9062 17.8789 11.5312ZM37.7305 15.0703V5.32031H39.9102V18H37.8359L37.7305 15.0703ZM38.1406 12.3984L39.043 12.375C39.043 13.2188 38.9531 14 38.7734 14.7188C38.6016 15.4297 38.3203 16.0469 37.9297 16.5703C37.5391 17.0938 37.0273 17.5039 36.3945 17.8008C35.7617 18.0898 34.9922 18.2344 34.0859 18.2344C33.4688 18.2344 32.9023 18.1445 32.3867 17.9648C31.8789 17.7852 31.4414 17.5078 31.0742 17.1328C30.707 16.7578 30.4219 16.2695 30.2188 15.668C30.0234 15.0664 29.9258 14.3438 29.9258 13.5V5.32031H32.0938V13.5234C32.0938 14.0938 32.1562 14.5664 32.2812 14.9414C32.4141 15.3086 32.5898 15.6016 32.8086 15.8203C33.0352 16.0312 33.2852 16.1797 33.5586 16.2656C33.8398 16.3516 34.1289 16.3945 34.4258 16.3945C35.3477 16.3945 36.0781 16.2188 36.6172 15.8672C37.1562 15.5078 37.543 15.0273 37.7773 14.4258C38.0195 13.8164 38.1406 13.1406 38.1406 12.3984ZM45.3828 7.3125V18H43.2148V5.32031H45.3242L45.3828 7.3125ZM49.3438 5.25L49.332 7.26562C49.1523 7.22656 48.9805 7.20312 48.8164 7.19531C48.6602 7.17969 48.4805 7.17188 48.2773 7.17188C47.7773 7.17188 47.3359 7.25 46.9531 7.40625C46.5703 7.5625 46.2461 7.78125 45.9805 8.0625C45.7148 8.34375 45.5039 8.67969 45.3477 9.07031C45.1992 9.45312 45.1016 9.875 45.0547 10.3359L44.4453 10.6875C44.4453 9.92188 44.5195 9.20312 44.668 8.53125C44.8242 7.85938 45.0625 7.26562 45.3828 6.75C45.7031 6.22656 46.1094 5.82031 46.6016 5.53125C47.1016 5.23438 47.6953 5.08594 48.3828 5.08594C48.5391 5.08594 48.7188 5.10547 48.9219 5.14453C49.125 5.17578 49.2656 5.21094 49.3438 5.25ZM58.7305 14.6367C58.7305 14.3242 58.6602 14.0352 58.5195 13.7695C58.3867 13.4961 58.1094 13.25 57.6875 13.0312C57.2734 12.8047 56.6484 12.6094 55.8125 12.4453C55.1094 12.2969 54.4727 12.1211 53.9023 11.918C53.3398 11.7148 52.8594 11.4688 52.4609 11.1797C52.0703 10.8906 51.7695 10.5508 51.5586 10.1602C51.3477 9.76953 51.2422 9.3125 51.2422 8.78906C51.2422 8.28906 51.3516 7.81641 51.5703 7.37109C51.7969 6.92578 52.1133 6.53125 52.5195 6.1875C52.9336 5.84375 53.4297 5.57422 54.0078 5.37891C54.5859 5.18359 55.2305 5.08594 55.9414 5.08594C56.957 5.08594 57.8242 5.26562 58.543 5.625C59.2617 5.98438 59.8125 6.46484 60.1953 7.06641C60.5781 7.66016 60.7695 8.32031 60.7695 9.04688H58.6016C58.6016 8.69531 58.4961 8.35547 58.2852 8.02734C58.082 7.69141 57.7812 7.41406 57.3828 7.19531C56.9922 6.97656 56.5117 6.86719 55.9414 6.86719C55.3398 6.86719 54.8516 6.96094 54.4766 7.14844C54.1094 7.32812 53.8398 7.55859 53.668 7.83984C53.5039 8.12109 53.4219 8.41797 53.4219 8.73047C53.4219 8.96484 53.4609 9.17578 53.5391 9.36328C53.625 9.54297 53.7734 9.71094 53.9844 9.86719C54.1953 10.0156 54.4922 10.1562 54.875 10.2891C55.2578 10.4219 55.7461 10.5547 56.3398 10.6875C57.3789 10.9219 58.2344 11.2031 58.9062 11.5312C59.5781 11.8594 60.0781 12.2617 60.4062 12.7383C60.7344 13.2148 60.8984 13.793 60.8984 14.4727C60.8984 15.0273 60.7812 15.5352 60.5469 15.9961C60.3203 16.457 59.9883 16.8555 59.5508 17.1914C59.1211 17.5195 58.6055 17.7773 58.0039 17.9648C57.4102 18.1445 56.7422 18.2344 56 18.2344C54.8828 18.2344 53.9375 18.0352 53.1641 17.6367C52.3906 17.2383 51.8047 16.7227 51.4062 16.0898C51.0078 15.457 50.8086 14.7891 50.8086 14.0859H52.9883C53.0195 14.6797 53.1914 15.1523 53.5039 15.5039C53.8164 15.8477 54.1992 16.0938 54.6523 16.2422C55.1055 16.3828 55.5547 16.4531 56 16.4531C56.5938 16.4531 57.0898 16.375 57.4883 16.2188C57.8945 16.0625 58.2031 15.8477 58.4141 15.5742C58.625 15.3008 58.7305 14.9883 58.7305 14.6367ZM69.0078 18.2344C68.125 18.2344 67.3242 18.0859 66.6055 17.7891C65.8945 17.4844 65.2812 17.0586 64.7656 16.5117C64.2578 15.9648 63.8672 15.3164 63.5938 14.5664C63.3203 13.8164 63.1836 12.9961 63.1836 12.1055V11.6133C63.1836 10.582 63.3359 9.66406 63.6406 8.85938C63.9453 8.04688 64.3594 7.35938 64.8828 6.79688C65.4062 6.23438 66 5.80859 66.6641 5.51953C67.3281 5.23047 68.0156 5.08594 68.7266 5.08594C69.6328 5.08594 70.4141 5.24219 71.0703 5.55469C71.7344 5.86719 72.2773 6.30469 72.6992 6.86719C73.1211 7.42188 73.4336 8.07812 73.6367 8.83594C73.8398 9.58594 73.9414 10.4062 73.9414 11.2969V12.2695H64.4727V10.5H71.7734V10.3359C71.7422 9.77344 71.625 9.22656 71.4219 8.69531C71.2266 8.16406 70.9141 7.72656 70.4844 7.38281C70.0547 7.03906 69.4688 6.86719 68.7266 6.86719C68.2344 6.86719 67.7812 6.97266 67.3672 7.18359C66.9531 7.38672 66.5977 7.69141 66.3008 8.09766C66.0039 8.50391 65.7734 9 65.6094 9.58594C65.4453 10.1719 65.3633 10.8477 65.3633 11.6133V12.1055C65.3633 12.707 65.4453 13.2734 65.6094 13.8047C65.7812 14.3281 66.0273 14.7891 66.3477 15.1875C66.6758 15.5859 67.0703 15.8984 67.5312 16.125C68 16.3516 68.5312 16.4648 69.125 16.4648C69.8906 16.4648 70.5391 16.3086 71.0703 15.9961C71.6016 15.6836 72.0664 15.2656 72.4648 14.7422L73.7773 15.7852C73.5039 16.1992 73.1562 16.5938 72.7344 16.9688C72.3125 17.3438 71.793 17.6484 71.1758 17.8828C70.5664 18.1172 69.8438 18.2344 69.0078 18.2344ZM83.8555 14.6367C83.8555 14.3242 83.7852 14.0352 83.6445 13.7695C83.5117 13.4961 83.2344 13.25 82.8125 13.0312C82.3984 12.8047 81.7734 12.6094 80.9375 12.4453C80.2344 12.2969 79.5977 12.1211 79.0273 11.918C78.4648 11.7148 77.9844 11.4688 77.5859 11.1797C77.1953 10.8906 76.8945 10.5508 76.6836 10.1602C76.4727 9.76953 76.3672 9.3125 76.3672 8.78906C76.3672 8.28906 76.4766 7.81641 76.6953 7.37109C76.9219 6.92578 77.2383 6.53125 77.6445 6.1875C78.0586 5.84375 78.5547 5.57422 79.1328 5.37891C79.7109 5.18359 80.3555 5.08594 81.0664 5.08594C82.082 5.08594 82.9492 5.26562 83.668 5.625C84.3867 5.98438 84.9375 6.46484 85.3203 7.06641C85.7031 7.66016 85.8945 8.32031 85.8945 9.04688H83.7266C83.7266 8.69531 83.6211 8.35547 83.4102 8.02734C83.207 7.69141 82.9062 7.41406 82.5078 7.19531C82.1172 6.97656 81.6367 6.86719 81.0664 6.86719C80.4648 6.86719 79.9766 6.96094 79.6016 7.14844C79.2344 7.32812 78.9648 7.55859 78.793 7.83984C78.6289 8.12109 78.5469 8.41797 78.5469 8.73047C78.5469 8.96484 78.5859 9.17578 78.6641 9.36328C78.75 9.54297 78.8984 9.71094 79.1094 9.86719C79.3203 10.0156 79.6172 10.1562 80 10.2891C80.3828 10.4219 80.8711 10.5547 81.4648 10.6875C82.5039 10.9219 83.3594 11.2031 84.0312 11.5312C84.7031 11.8594 85.2031 12.2617 85.5312 12.7383C85.8594 13.2148 86.0234 13.793 86.0234 14.4727C86.0234 15.0273 85.9062 15.5352 85.6719 15.9961C85.4453 16.457 85.1133 16.8555 84.6758 17.1914C84.2461 17.5195 83.7305 17.7773 83.1289 17.9648C82.5352 18.1445 81.8672 18.2344 81.125 18.2344C80.0078 18.2344 79.0625 18.0352 78.2891 17.6367C77.5156 17.2383 76.9297 16.7227 76.5312 16.0898C76.1328 15.457 75.9336 14.7891 75.9336 14.0859H78.1133C78.1445 14.6797 78.3164 15.1523 78.6289 15.5039C78.9414 15.8477 79.3242 16.0938 79.7773 16.2422C80.2305 16.3828 80.6797 16.4531 81.125 16.4531C81.7188 16.4531 82.2148 16.375 82.6133 16.2188C83.0195 16.0625 83.3281 15.8477 83.5391 15.5742C83.75 15.3008 83.8555 14.9883 83.8555 14.6367Z" fill="#8A8A8A"/>
            //         </front_png>
            //     </a>
            //     </div>
            // </Menu>
            :
            <Menu>
                <a href={'/login'} style={{marginRight: 10}}>Login</a>
                <a href={'/signup'}>Sign up</a>
            </Menu>

    )
}

export default NavbarContainer;