import React from "react";
import styles from './css/pageNotFound.module.css'
// import {useRouterContext} from "../api/RouterProvider";
import {useNavigate} from "react-router";

const PageNotFoundContainer = () => {
    const navigate = useNavigate();
    // const {from} = useRouterContext()
    // console.log(from)
    return (
        <div>
            <div className={styles.TryAgain}>Try again or go back to the main menu</div>
            <div className={styles.ErrorCode}>404</div>
            <div className={styles.SWW}>SOMETHING WENT WRONG</div>
            <div className={styles.buttonGroup}>
                <div className={styles.buttonMainMenu} onClick={() => {navigate(-1)}}/>
                <p className={styles.buttonText} style={{background: 'black'}}> BACK TO THE MAIN MENU</p>
            </div>


        </div>
    )
};

export default PageNotFoundContainer;