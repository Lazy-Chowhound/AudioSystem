import React from "react";
import {Collapse, Drawer} from "antd";

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
            <Drawer title="扰动详解" placement="right" onClose={this.closeDrawer}
                    visible={this.state.visible}>
                <Collapse accordion>
                    <Panel header="Animal" key="Animal">
                        <Collapse accordion>
                            <Panel header="Pets" key="Pets">
                                <p>{"Pets"}</p>
                            </Panel>
                            <Panel header="Livestock" key="Livestock">
                                <p>{"Livestock"}</p>
                            </Panel>
                            <Panel header="Wild animals" key="Wild animals">
                                <p>{"Wild animals"}</p>
                            </Panel>
                        </Collapse>
                    </Panel>
                    <Panel header="Human sounds" key="Human sounds">
                        <Collapse accordion>
                            <Panel header="Human voice" key="Human voice">
                                <p>{"Human voice"}</p>
                            </Panel>
                            <Panel header="Whistling" key="Whistling">
                                <p>{"Whistling"}</p>
                            </Panel>
                            <Panel header="Respiratory sounds" key="Respiratory sounds">
                                <p>{"Respiratory sounds"}</p>
                            </Panel>
                            <Panel header="Human locomotion" key="Human locomotion">
                                <p>{"Human locomotion"}</p>
                            </Panel>
                            <Panel header="Digestive" key="Digestive">
                                <p>{"Digestive"}</p>
                            </Panel>
                            <Panel header="Hands" key="Hands">
                                <p>{"Hands"}</p>
                            </Panel>
                            <Panel header="Heartbeat" key="Heartbeat">
                                <p>{"Heartbeat"}</p>
                            </Panel>
                            <Panel header="Otoacoustic emission" key="Otoacoustic emission">
                                <p>{"Otoacoustic emission"}</p>
                            </Panel>
                            <Panel header="Human group actions" key="Human group actions">
                                <p>{"Human group actions"}</p>
                            </Panel>
                        </Collapse>
                    </Panel>
                    <Panel header="Music" key="Music">
                        <Collapse accordion>
                            <Panel header="Music instrument" key="Music instrument">
                                <p>{"Music instrument"}</p>
                            </Panel>
                            <Panel header="Music genre" key="Music genre">
                                <p>{"Music genre"}</p>
                            </Panel>
                            <Panel header="Music concepts" key="Music concepts">
                                <p>{"Music concepts"}</p>
                            </Panel>
                            <Panel header="Music role" key="Music role">
                                <p>{"Music role"}</p>
                            </Panel>
                            <Panel header="Music mood" key="Music mood">
                                <p>{"Music mood"}</p>
                            </Panel>
                        </Collapse>
                    </Panel>
                    <Panel header="Natural sounds" key="Natural sounds">
                        <Collapse accordion>
                            <Panel header="Wind" key="Wind">
                                <p>{"Wind"}</p>
                            </Panel>
                            <Panel header="Thunderstorm" key="Thunderstorm">
                                <p>{"Thunderstorm"}</p>
                            </Panel>
                            <Panel header="Fire" key="Fire">
                                <p>{"Fire"}</p>
                            </Panel>
                            <Panel header="Water" key="Water">
                                <p>{"Water"}</p>
                            </Panel>
                        </Collapse>
                    </Panel>
                    <Panel header="Sound level" key="Sound level">
                        <Collapse accordion>
                            <Panel header="Louder" key="Louder">
                                <p>{"Louder"}</p>
                            </Panel>
                            <Panel header="Quieter" key="Quieter">
                                <p>{"Quieter"}</p>
                            </Panel>
                            <Panel header="Pitch" key="Pitch">
                                <p>{"Pitch"}</p>
                            </Panel>
                            <Panel header="Faster" key="Faster">
                                <p>{"Faster"}</p>
                            </Panel>
                        </Collapse>
                    </Panel>
                    <Panel header="Sounds of things" key="Sounds of things">
                        <Collapse accordion>
                            <Panel header="Vehicle" key="Vehicle">
                                <p>{"Vehicle"}</p>
                            </Panel>
                            <Panel header="Engine" key="Engine">
                                <p>{"Engine"}</p>
                            </Panel>
                            <Panel header="Domestic sounds" key="Domestic sounds">
                                <p>{"Domestic sounds"}</p>
                            </Panel>
                            <Panel header="Bell" key="Bell">
                                <p>{"Bell"}</p>
                            </Panel>
                            <Panel header="Alarm" key="Alarm">
                                <p>{"Alarm"}</p>
                            </Panel>
                            <Panel header="Mechanisms" key="Mechanisms">
                                <p>{"Mechanisms"}</p>
                            </Panel>
                            <Panel header="Tools" key="Tools">
                                <p>{"Tools"}</p>
                            </Panel>
                            <Panel header="Explosion" key="Explosion">
                                <p>{"Explosion"}</p>
                            </Panel>
                            <Panel header="Wood" key="Wood">
                                <p>{"Wood"}</p>
                            </Panel>
                            <Panel header="Glass" key="Glass">
                                <p>{"Glass"}</p>
                            </Panel>
                            <Panel header="Liquid" key="Liquid">
                                <p>{"Liquid"}</p>
                            </Panel>
                            <Panel header="Miscellaneous sources" key="Miscellaneous sources">
                                <p>{"Miscellaneous sources"}</p>
                            </Panel>
                            <Panel header="Specific impact sounds" key="Specific impact sounds">
                                <p>{"Specific impact sounds"}</p>
                            </Panel>
                        </Collapse>
                    </Panel>
                    <Panel header="Source-ambiguous sounds" key="Source-ambiguous sounds">
                        <Collapse accordion>
                            <Panel header="Generic impact sounds" key="Generic impact sounds">
                                <p>{"Generic impact sounds"}</p>
                            </Panel>
                            <Panel header="Surface contact" key="Surface contact">
                                <p>{"Surface contact"}</p>
                            </Panel>
                            <Panel header="Deformable shell" key="Deformable shell">
                                <p>{"Deformable shell"}</p>
                            </Panel>
                            <Panel header="Onomatopoeia" key="Onomatopoeia">
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