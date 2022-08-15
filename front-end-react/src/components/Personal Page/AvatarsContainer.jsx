import React from "react";
import StaticAvatars from "../StaticRoutes";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import styles from '../css/avatarPP.module.css'

const AvatarsContainer = ({user}) => {
    const settings = {
    infinite: true,
    dots: true,
    slidesToShow: 1,
    arrows: false,
    slidesToScroll: 1,
    lazyLoad: true
  };
  return (
      user.href?
          <div className={styles.avatarSlider}>
          <Slider  {...settings} >
              {user.href.map((item, inx) => (
              <img key={inx} src={StaticAvatars.StaticAvatars + item}/>
              ))}
          </Slider>
              </div>
          :
          <></>
  );
    // return (
    //     <div>
    //         <Slider {...settings}>
    //             {user.href.map((avatar, inx) => {
    //             return <Image key={inx} src={StaticAvatars.StaticAvatars + avatar}/> })}
    //         </Slider>
            {/*<Image*/}
            {/*      preview={{visible: false}}*/}
            {/*      width={200}*/}
            {/*      src={StaticAvatars.StaticAvatars + user.href[0]}*/}
            {/*      onClick={() => setVisible(true)}*/}
            {/*/>*/}
            {/*<div style={{ display: 'none' }}>*/}
            {/*    <Image.PreviewGroup preview={{ visible: visible, onVisibleChange: vis => setVisible(vis) }}>*/}
            {/*        {user.href.map((avatar, inx) => {*/}
            {/*            console.log(StaticAvatars.StaticAvatars + avatar)*/}
            {/*            return <Image key={inx} src={StaticAvatars.StaticAvatars + avatar}/>*/}
            {/*        })}*/}
            {/*    </Image.PreviewGroup>*/}
            {/*</div>*/}
        // </div>
    // )
}

export default AvatarsContainer;