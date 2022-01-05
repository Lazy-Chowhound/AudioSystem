import React from "react";
import {Image} from "antd";

class ImageDisplay extends React.Component {

    render() {
        return (
            <Image width={550} src={this.props.src}/>
        )
    }
}

export default ImageDisplay