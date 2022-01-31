import React from "react";
import {Drawer} from "antd";

class PatternDrawer extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            visible: false
        }
    }

    componentDidMount() {
        this.props.bindChildren(this)
    }

    openDrawer = () => {
        this.setState({
            visible: true
        })
    }

    closeDrawer = () => {
        this.setState({
            visible: false
        })
    }

    render() {
        return (
            <Drawer title="扰动详解" placement="right" onClose={this.closeDrawer}
                    visible={this.state.visible}>
                <p>Some contents...</p>
            </Drawer>
        )
    }
}

export default PatternDrawer