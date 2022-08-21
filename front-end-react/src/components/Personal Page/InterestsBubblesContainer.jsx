import BubbleUI from "react-bubble-ui";
import "react-bubble-ui/dist/index.css";
import React, {useState} from "react";
import styles from '../css/bubbleUI.css'

const InterestsBubblesContainer = (props) => {

	const [data, setData] = useState(props.interest);
	const options = {
		size: 180,
		minSize: 20,
		gutter: 10,
		provideProps: true,
		numCols: 3,
		fringeWidth: 100,
		yRadius: 220,
		xRadius: 130,
		cornerRadius: 50,
		showGuides: false,
		compact: true,
		gravitation: 0
	}
	// console.log(props)

	const needColor = (sphere) => {
		if (sphere === "Business and Financial Operations") {
			return '#fce2fb'
		} else if (sphere === "Educational Instruction and Library") {
			return '#fef5ee'
		} else if (sphere === "Protective Service") {
			return '#932598'
		} else if (sphere === "Community and Social Service") {
			return '#c91367'
		} else if (sphere === "Healthcare Support") {
			return '#380a8a'
		}
	}

	const BubData = (interest) => {
		return (
			<div
      style={{
        backgroundColor: needColor(interest.sphere_name),
      }}
      className={styles.childComponent}
    >
      {(
		  <div
			  style={{
				  display: "flex",
				  justifyContent: "center",
				  alignItems: "center",
				  flexDirection: "column",
				  transition: "opacity 0.1s ease",
				  opacity: 0.5,
				  pointerEvents: "none",
			  }}
		  ><p
			  style={{
				  color: 'green',
				  fontSize: 14,
				  marginBottom: 6,
				  fontWeight: 1000,
				  maxWidth: 150,
				  textAlign: "center",
			  }}
		  >
			  {interest.sphere_name}
		  </p>
			  <p
				  style={{
					  color: 'green',
					  fontSize: 14,
					  marginBottom: 5,
					  maxWidth: 100,
					  opacity: 0.5,
				  }}
			  >
				  {interest.count_achievements}
			  </p>
		  </div>
	  )}
    </div>
			)
	}
	console.log(data)
	console.log(data[0])
	// const getBubbles = () => {
	// 	data.map((interest, index) => {
    //                     return (
    //                         <BubData {...interest} key={index}/>
    //                     )
    //                 })
	// };
	//
    // const bubbles = getBubbles();
	//
	// console.log(bubbles)

	return (
             <BubbleUI options={options} className={styles.myBubbleUI} style={{width: 1000, height: 600}}>
				 {/*{bubbles}*/}
				 {data?
					 data.map((interest, index) => {
						return <BubData {...interest} key={index}/>
					})
					:
					<></>}
             </BubbleUI>
             )
};

export default InterestsBubblesContainer;