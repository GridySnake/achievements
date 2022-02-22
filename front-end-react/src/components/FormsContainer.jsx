import React from "react";

const FormsContainer = ({menuState}) => {
    if (menuState === 0) {
        return (
            <div>
                Dropdown
            </div>
        )
    } else if (menuState === 1) {
        return (
            <div>
                Form
            </div>
        )
    } else {
        return (
            <div>
                Lol
            </div>
        )
    }
}

export default FormsContainer