import React from "react";
import StaticAvatars from "../StaticRoutes";
import {Image} from "antd";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";

const AvatarsContainer = ({user, visible, setVisible}) => {
    const settings = {
    infinite: true,
    dots: true,
    slidesToShow: 1,
    arrows: false,
    slidesToScroll: 1,
    lazyLoad: true
  };
  return (
    <div>
      <Slider {...settings}>
          {user.href.map((item, inx) => (
        <div key={inx}>
          <img src={StaticAvatars.StaticAvatars + item} style={{width: "405px", height: "540px"}}/>
        </div>))}
      </Slider>
    </div>
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