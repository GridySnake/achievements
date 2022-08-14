import React from "react";

import styles from "./css/footer.module.css";
import StaticFrontPng from './StaticRoutes';

const FooterContainer = () => {

    const StaticFront = StaticFrontPng.StaticFrontPng

    return (
        <div className={styles.footerDiv}>
            <div className={styles.logoDiv}>
                <div className={styles.layer2Div}>
                    <i className={styles.aCHI}>ACHI</i>
                    <img className={styles.layer1Icon} alt="" src={StaticFront + 'footer_logo.png'} />
                </div>
            </div>
            <div className={styles.rectangleDiv} />
            <div className={styles.achiCreativeDiv}>Achi Creative</div>
            <div className={styles.supportDiv}>Support</div>
            <div className={styles.aboutDiv}>About</div>
            <div className={styles.fAQDiv}>F.A.Q.</div>
            <div className={styles.div}>2022</div>
            <img className={styles.bxbxCopyrightIcon} alt="" src={StaticFront + 'copyright.png'}/>
            <div className={styles.lineDiv} />
            <div className={styles.lineDiv1} />
            <div className={styles.sUPPORTOURCOMMUNITY}>SUPPORT OUR COMMUNITY</div>
            <img className={styles.groupIcon} alt="" src={StaticFront + 'twitter.png'} />
            <img className={styles.akarIconsfacebookFill} alt="" src={StaticFront + 'facebook.png'}/>
            <img className={styles.cibvkIcon} alt="" src={StaticFront + 'vk.png'} />
            <img className={styles.biinstagramIcon} alt="" src={StaticFront + 'insta.png'} />
        </div>
    )
};

export default FooterContainer;