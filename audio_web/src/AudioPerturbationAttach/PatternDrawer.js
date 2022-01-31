import React from "react";
import {Collapse, Drawer} from "antd";
import {CaretRightOutlined} from "@ant-design/icons";
import "../css/PatternDrawer.css"

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
        const {Panel} = Collapse;
        return (
            <Drawer title="扰动详解" width={480} placement="right" onClose={this.closeDrawer}
                    visible={this.state.visible}>
                <Collapse accordion bordered={false}
                          expandIcon={({isActive}) => <CaretRightOutlined rotate={isActive ? 90 : 0}/>}
                          className="site-collapse-custom-collapse">
                    <Panel header="Animal" key="Animal" className="site-collapse-custom-panel">
                        <Collapse accordion bordered={false}
                                  expandIcon={({isActive}) => <CaretRightOutlined rotate={isActive ? 90 : 0}/>}>
                            <Panel header="Pets" key="Pets" className="site-collapse-custom-panel">
                                <p>{"Pets"}</p>
                            </Panel>
                            <Panel header="Livestock" key="Livestock" className="site-collapse-custom-panel">
                                <p>{"Livestock"}</p>
                            </Panel>
                            <Panel header="Wild animals" key="Wild animals" className="site-collapse-custom-panel">
                                <p>{"Wild animals"}</p>
                            </Panel>
                        </Collapse>
                    </Panel>
                    <Panel header="Gaussian noise" key="Gaussian noise" className="site-collapse-custom-panel">
                        <p>{"Gaussian noise"}</p>
                    </Panel>
                    <Panel header="Human sounds" key="Human sounds" className="site-collapse-custom-panel">
                        <Collapse accordion bordered={false}
                                  expandIcon={({isActive}) => <CaretRightOutlined rotate={isActive ? 90 : 0}/>}>
                            <Panel header="Human voice" key="Human voice" className="site-collapse-custom-panel">
                                <p>{"Human voice"}</p>
                            </Panel>
                            <Panel header="Whistling" key="Whistling" className="site-collapse-custom-panel">
                                <p>{"Whistling"}</p>
                            </Panel>
                            <Panel header="Respiratory sounds" key="Respiratory sounds"
                                   className="site-collapse-custom-panel">
                                <p>{"Respiratory sounds"}</p>
                            </Panel>
                            <Panel header="Human locomotion" key="Human locomotion"
                                   className="site-collapse-custom-panel">
                                <p>{"Human locomotion"}</p>
                            </Panel>
                            <Panel header="Digestive" key="Digestive" className="site-collapse-custom-panel">
                                <p>{"Digestive"}</p>
                            </Panel>
                            <Panel header="Hands" key="Hands" className="site-collapse-custom-panel">
                                <p>{"Hands"}</p>
                            </Panel>
                            <Panel header="Heartbeat" key="Heartbeat" className="site-collapse-custom-panel">
                                <p>{"Heartbeat"}</p>
                            </Panel>
                            <Panel header="Otoacoustic emission" key="Otoacoustic emission"
                                   className="site-collapse-custom-panel">
                                <p>{"Otoacoustic emission"}</p>
                            </Panel>
                            <Panel header="Human group actions" key="Human group actions"
                                   className="site-collapse-custom-panel">
                                <p>{"Human group actions"}</p>
                            </Panel>
                        </Collapse>
                    </Panel>
                    <Panel header="Music" key="Music" className="site-collapse-custom-panel">
                        <Collapse accordion bordered={false}
                                  expandIcon={({isActive}) => <CaretRightOutlined rotate={isActive ? 90 : 0}/>}>
                            <Panel header="Music instrument" key="Music instrument"
                                   className="site-collapse-custom-panel">
                                <p>{"Music instrument"}</p>
                            </Panel>
                            <Panel header="Music genre" key="Music genre" className="site-collapse-custom-panel">
                                <p>{"Music genre"}</p>
                            </Panel>
                            <Panel header="Music concepts" key="Music concepts" className="site-collapse-custom-panel">
                                <p>{"Music concepts"}</p>
                            </Panel>
                            <Panel header="Music role" key="Music role" className="site-collapse-custom-panel">
                                <p>{"Music role"}</p>
                            </Panel>
                            <Panel header="Music mood" key="Music mood" className="site-collapse-custom-panel">
                                <p>{"Music mood"}</p>
                            </Panel>
                        </Collapse>
                    </Panel>
                    <Panel header="Natural sounds" key="Natural sounds" className="site-collapse-custom-panel">
                        <Collapse accordion bordered={false}
                                  expandIcon={({isActive}) => <CaretRightOutlined rotate={isActive ? 90 : 0}/>}>
                            <Panel header="Wind" key="Wind" className="site-collapse-custom-panel">
                                <p>{"Wind"}</p>
                            </Panel>
                            <Panel header="Thunderstorm" key="Thunderstorm" className="site-collapse-custom-panel">
                                <p>{"Thunderstorm"}</p>
                            </Panel>
                            <Panel header="Fire" key="Fire" className="site-collapse-custom-panel">
                                <p>{"Fire"}</p>
                            </Panel>
                            <Panel header="Water" key="Water" className="site-collapse-custom-panel">
                                <p>{"Water"}</p>
                            </Panel>
                        </Collapse>
                    </Panel>
                    <Panel header="Sound level" key="Sound level" className="site-collapse-custom-panel">
                        <Collapse accordion bordered={false}
                                  expandIcon={({isActive}) => <CaretRightOutlined rotate={isActive ? 90 : 0}/>}>
                            <Panel header="Louder" key="Louder" className="site-collapse-custom-panel">
                                <p>{"Louder"}</p>
                            </Panel>
                            <Panel header="Quieter" key="Quieter" className="site-collapse-custom-panel">
                                <p>{"Quieter"}</p>
                            </Panel>
                            <Panel header="Pitch" key="Pitch" className="site-collapse-custom-panel">
                                <p>{"Pitch"}</p>
                            </Panel>
                            <Panel header="Faster" key="Faster" className="site-collapse-custom-panel">
                                <p>{"Faster"}</p>
                            </Panel>
                        </Collapse>
                    </Panel>
                    <Panel header="Sounds of things" key="Sounds of things" className="site-collapse-custom-panel">
                        <Collapse accordion bordered={false}
                                  expandIcon={({isActive}) => <CaretRightOutlined rotate={isActive ? 90 : 0}/>}>
                            <Panel header="Vehicle" key="Vehicle" className="site-collapse-custom-panel">
                                <p>{"Vehicle"}</p>
                            </Panel>
                            <Panel header="Engine" key="Engine" className="site-collapse-custom-panel">
                                <p>{"Engine"}</p>
                            </Panel>
                            <Panel header="Domestic sounds" key="Domestic sounds"
                                   className="site-collapse-custom-panel">
                                <p>{"Domestic sounds"}</p>
                            </Panel>
                            <Panel header="Bell" key="Bell" className="site-collapse-custom-panel">
                                <p>{"Bell"}</p>
                            </Panel>
                            <Panel header="Alarm" key="Alarm" className="site-collapse-custom-panel">
                                <p>{"Alarm"}</p>
                            </Panel>
                            <Panel header="Mechanisms" key="Mechanisms" className="site-collapse-custom-panel">
                                <p>{"Mechanisms"}</p>
                            </Panel>
                            <Panel header="Tools" key="Tools" className="site-collapse-custom-panel">
                                <p>{"Tools"}</p>
                            </Panel>
                            <Panel header="Explosion" key="Explosion" className="site-collapse-custom-panel">
                                <p>{"Explosion"}</p>
                            </Panel>
                            <Panel header="Wood" key="Wood" className="site-collapse-custom-panel">
                                <p>{"Wood"}</p>
                            </Panel>
                            <Panel header="Glass" key="Glass" className="site-collapse-custom-panel">
                                <p>{"Glass"}</p>
                            </Panel>
                            <Panel header="Liquid" key="Liquid" className="site-collapse-custom-panel">
                                <p>{"Liquid"}</p>
                            </Panel>
                            <Panel header="Miscellaneous sources" key="Miscellaneous sources"
                                   className="site-collapse-custom-panel">
                                <p>{"Miscellaneous sources"}</p>
                            </Panel>
                            <Panel header="Specific impact sounds" key="Specific impact sounds"
                                   className="site-collapse-custom-panel">
                                <p>{"Specific impact sounds"}</p>
                            </Panel>
                        </Collapse>
                    </Panel>
                    <Panel header="Source-ambiguous sounds" key="Source-ambiguous sounds"
                           className="site-collapse-custom-panel">
                        <Collapse accordion bordered={false}
                                  expandIcon={({isActive}) => <CaretRightOutlined rotate={isActive ? 90 : 0}/>}>
                            <Panel header="Generic impact sounds" key="Generic impact sounds"
                                   className="site-collapse-custom-panel">
                                <p>{"Generic impact sounds"}</p>
                            </Panel>
                            <Panel header="Surface contact" key="Surface contact"
                                   className="site-collapse-custom-panel">
                                <p>{"Surface contact"}</p>
                            </Panel>
                            <Panel header="Deformable shell" key="Deformable shell"
                                   className="site-collapse-custom-panel">
                                <p>{"Deformable shell"}</p>
                            </Panel>
                            <Panel header="Onomatopoeia" key="Onomatopoeia" className="site-collapse-custom-panel">
                                <p>{"Onomatopoeia"}</p>
                            </Panel>
                        </Collapse>
                    </Panel>
                </Collapse>
            </Drawer>
        )
    }
}

export default PatternDrawer