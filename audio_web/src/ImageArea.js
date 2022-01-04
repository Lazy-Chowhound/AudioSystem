import React from "react";
import {Image, message} from "antd";

class ImageArea extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            url: null
        };
    }

    componentDidMount() {
        // console.log(this.props.src)
        // this.state = {
        //     url: this.props.src
        // };
        // console.log(this.state.url)
    }

    render() {
        return (
            <Image
                width={450}
                src={this.props.src}
            />
        )
    }
}

export default ImageArea