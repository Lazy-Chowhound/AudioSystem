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

    formatText = (text) => {
        return "       " + text;
    }

    render() {
        const {Panel} = Collapse;
        return (
            <Drawer title="扰动类别" width={480} placement="right" onClose={this.closeDrawer}
                    visible={this.state.visible}>
                <Collapse accordion bordered={false}
                          expandIcon={({isActive}) => <CaretRightOutlined rotate={isActive ? 90 : 0}/>}
                          className="site-collapse-custom-collapse">
                    <Panel style={{whiteSpace: "pre-wrap"}} header="Animal" key="Animal"
                           className="site-collapse-custom-panel">
                        <p>{this.formatText("由非人类动物的身体和动作产生的所有声音")}</p>
                        <Collapse accordion bordered={false}
                                  expandIcon={({isActive}) => <CaretRightOutlined rotate={isActive ? 90 : 0}/>}>
                            <Panel style={{whiteSpace: "pre-wrap"}} header="Pets" key="Pets"
                                   className="site-collapse-custom-panel">
                                <p>{this.formatText("为了陪伴、保护和娱乐而和人类保持亲密的动物的声音")}</p>
                            </Panel>
                            <Panel style={{whiteSpace: "pre-wrap"}} header="Livestock" key="Livestock"
                                   className="site-collapse-custom-panel">
                                <p>{this.formatText("与农场和农业有关的动物发出的声音")}</p>
                            </Panel>
                            <Panel style={{whiteSpace: "pre-wrap"}} header="Wild animals" key="Wild animals"
                                   className="site-collapse-custom-panel">
                                <p>{this.formatText("通常不由人类抚养的动物发出的声音")}</p>
                            </Panel>
                        </Collapse>
                    </Panel>
                    <Panel style={{whiteSpace: "pre-wrap"}} header="Gaussian noise" key="Gaussian noise"
                           className="site-collapse-custom-panel">
                        <p>{this.formatText("高斯噪声。如果一个噪声，它的幅度分布服从高斯分布，而它的功率谱密度又是均匀分布的，则称它为高斯噪声")}</p>
                    </Panel>
                    <Panel header="Human sounds" key="Human sounds" className="site-collapse-custom-panel">
                        <Collapse accordion bordered={false}
                                  expandIcon={({isActive}) => <CaretRightOutlined rotate={isActive ? 90 : 0}/>}>
                            <p>{this.formatText("人体通过个体的动作产生的声音")}</p>
                            <Panel style={{whiteSpace: "pre-wrap"}} header="Human voice" key="Human voice"
                                   className="site-collapse-custom-panel">
                                <p>{this.formatText("人声由人使用声带发出的声音组成，用于说话、唱歌、大笑、哭泣、尖叫等")}</p>
                            </Panel>
                            <Panel style={{whiteSpace: "pre-wrap"}} header="Whistling" key="Whistling"
                                   className="site-collapse-custom-panel">
                                <p>{this.formatText("通过双唇之间的小开口吹气或吸入空气产生的高音调")}</p>
                            </Panel>
                            <Panel style={{whiteSpace: "pre-wrap"}} header="Respiratory sounds" key="Respiratory sounds"
                                   className="site-collapse-custom-panel">
                                <p>{this.formatText("空气通过呼吸系统（鼻子、嘴巴、气管和肺）运动产生的声音")}</p>
                            </Panel>
                            <Panel style={{whiteSpace: "pre-wrap"}} header="Human locomotion" key="Human locomotion"
                                   className="site-collapse-custom-panel">
                                <p>{this.formatText("改变位置所涉及的人体动作产生的声音")}</p>
                            </Panel>
                            <Panel style={{whiteSpace: "pre-wrap"}} header="Digestive" key="Digestive"
                                   className="site-collapse-custom-panel">
                                <p>{this.formatText("与人类进食和处理营养或食物功能相关的声音")}</p>
                            </Panel>
                            <Panel style={{whiteSpace: "pre-wrap"}} header="Hands" key="Hands"
                                   className="site-collapse-custom-panel">
                                <p>{this.formatText("人类的手和手指发出的声音")}</p>
                            </Panel>
                            <Panel style={{whiteSpace: "pre-wrap"}} header="Heartbeat" key="Heartbeat"
                                   className="site-collapse-custom-panel">
                                <p>{this.formatText("心脏跳动以及由此产生的血液流过它从而发出的声音")}</p>
                            </Panel>
                            <Panel style={{whiteSpace: "pre-wrap"}} header="Otoacoustic emission"
                                   key="Otoacoustic emission"
                                   className="site-collapse-custom-panel">
                                <p>{this.formatText("在内耳内产生的声音，通常被认为是由高度敏感的耳朵机制中的正反馈产生的")}</p>
                            </Panel>
                            <Panel style={{whiteSpace: "pre-wrap"}} header="Human group actions"
                                   key="Human group actions"
                                   className="site-collapse-custom-panel">
                                <p>{this.formatText("由人类群体而不是个人产生的声音")}</p>
                            </Panel>
                        </Collapse>
                    </Panel>
                    <Panel style={{whiteSpace: "pre-wrap"}} header="Music" key="Music"
                           className="site-collapse-custom-panel">
                        <p>{this.formatText("音乐是一种以声音和沉默为媒介的艺术形式和文化活动。音乐的共同元素是音高、节奏、动感以及音色和纹理的声音品质")}</p>
                        <Collapse accordion bordered={false}
                                  expandIcon={({isActive}) => <CaretRightOutlined rotate={isActive ? 90 : 0}/>}>
                            <Panel style={{whiteSpace: "pre-wrap"}} header="Musical instrument" key="Musical instrument"
                                   className="site-collapse-custom-panel">
                                <p>{this.formatText("与创建、改编或以其他方式用于发出音乐声音的乐器特别相关的声音")}</p>
                            </Panel>
                            <Panel style={{whiteSpace: "pre-wrap"}} header="Music genre" key="Music genre"
                                   className="site-collapse-custom-panel">
                                <p>{this.formatText("代表音乐风格或分类的类别，可用于识别和组织类似的音乐艺术家或录音，如流行音乐、摇滚乐、节奏布鲁斯等等")}</p>
                            </Panel>
                            <Panel style={{whiteSpace: "pre-wrap"}} header="Musical concepts" key="Musical concepts"
                                   className="site-collapse-custom-panel">
                                <p>{this.formatText("用于描述反映其抽象音乐理论属性而不是其物理实现的音乐声音、如节奏、鼓点、和弦等")}</p>
                            </Panel>
                            <Panel style={{whiteSpace: "pre-wrap"}} header="Music role" key="Music role"
                                   className="site-collapse-custom-panel">
                                <p>{this.formatText("听众将能够认识到音乐将被用于什么场合，根据音乐的功能角色来描述音乐。如背景音乐、原声音乐、舞曲等")}</p>
                            </Panel>
                            <Panel style={{whiteSpace: "pre-wrap"}} header="Music mood" key="Music mood"
                                   className="site-collapse-custom-panel">
                                <p>{this.formatText("不论流派或乐器，表示音乐对于情感的影响的类别。如激情的音乐、舒缓的音乐")}</p>
                            </Panel>
                        </Collapse>
                    </Panel>
                    <Panel style={{whiteSpace: "pre-wrap"}} header="Natural sounds" key="Natural sounds"
                           className="site-collapse-custom-panel">
                        <Collapse accordion bordered={false}
                                  expandIcon={({isActive}) => <CaretRightOutlined rotate={isActive ? 90 : 0}/>}>
                            <p>{this.formatText("在正常音景下由自然来源发出的声音,不包括动物和人类的声音")}</p>
                            <Panel style={{whiteSpace: "pre-wrap"}} header="Wind" key="Wind"
                                   className="site-collapse-custom-panel">
                                <p>{this.formatText("由大规模气体流动引起的声音，尤其是在地球表面流动的空气")}</p>
                            </Panel>
                            <Panel style={{whiteSpace: "pre-wrap"}} header="Thunderstorm" key="Thunderstorm"
                                   className="site-collapse-custom-panel">
                                <p>{this.formatText("以闪电的存在及其对地球大气的声学影响为特征的风暴的声音，称为雷声")}</p>
                            </Panel>
                            <Panel style={{whiteSpace: "pre-wrap"}} header="Fire" key="Fire"
                                   className="site-collapse-custom-panel">
                                <p>{this.formatText("材料在燃烧的放热化学过程中释放热量、光和各种反应产物，快速氧化产生的声音")}</p>
                            </Panel>
                            <Panel style={{whiteSpace: "pre-wrap"}} header="Water" key="Water"
                                   className="site-collapse-custom-panel">
                                <p>{"液态水运动引起的声音"}</p>
                            </Panel>
                        </Collapse>
                    </Panel>
                    <Panel style={{whiteSpace: "pre-wrap"}} header="Sound level" key="Sound level"
                           className="site-collapse-custom-panel">
                        <p>{this.formatText("改变声音的基本元素")}</p>
                        <Collapse accordion bordered={false}
                                  expandIcon={({isActive}) => <CaretRightOutlined rotate={isActive ? 90 : 0}/>}>
                            <Panel style={{whiteSpace: "pre-wrap"}} header="Louder" key="Louder"
                                   className="site-collapse-custom-panel">
                                <p>{"使声音的响度更大"}</p>
                            </Panel>
                            <Panel style={{whiteSpace: "pre-wrap"}} header="Quieter" key="Quieter"
                                   className="site-collapse-custom-panel">
                                <p>{"使声音的响度更小"}</p>
                            </Panel>
                            <Panel style={{whiteSpace: "pre-wrap"}} header="Pitch" key="Pitch"
                                   className="site-collapse-custom-panel">
                                <p>{"改变声音的音调高低"}</p>
                            </Panel>
                            <Panel style={{whiteSpace: "pre-wrap"}} header="Speed" key="Speed"
                                   className="site-collapse-custom-panel">
                                <p>{"倍速播放"}</p>
                            </Panel>
                        </Collapse>
                    </Panel>
                    <Panel style={{whiteSpace: "pre-wrap"}} header="Sound of things" key="Sounds of things"
                           className="site-collapse-custom-panel">
                        <p>{this.formatText("听众能够立即明白由声音是由何种特定对象发出的一组声音类别（而不是更字面意义上的“声音”）")}</p>
                        <Collapse accordion bordered={false}
                                  expandIcon={({isActive}) => <CaretRightOutlined rotate={isActive ? 90 : 0}/>}>
                            <Panel style={{whiteSpace: "pre-wrap"}} header="Vehicle" key="Vehicle"
                                   className="site-collapse-custom-panel">
                                <p>{this.formatText("由运送人员或货物的移动机器发出的声音")}</p>
                            </Panel>
                            <Panel style={{whiteSpace: "pre-wrap"}} header="Engine" key="Engine"
                                   className="site-collapse-custom-panel">
                                <p>{this.formatText("用于产生机械能的机器的声音")}</p>
                            </Panel>
                            <Panel style={{whiteSpace: "pre-wrap"}} header="Domestic sounds" key="Domestic sounds"
                                   className="site-collapse-custom-panel">
                                <p>{this.formatText("在家中录制的声音")}</p>
                            </Panel>
                            <Panel style={{whiteSpace: "pre-wrap"}} header="Bell" key="Bell"
                                   className="site-collapse-custom-panel">
                                <p>{this.formatText("一种简单乐器的声音，通常由铸成空心杯形状的金属组成，其侧面形成一个共鸣器，当被悬挂在其中的“拍板”或单独的木槌或锤子敲击时，共鸣器会以单一音调振动")}</p>
                            </Panel>
                            <Panel style={{whiteSpace: "pre-wrap"}} header="Alarm" key="Alarm"
                                   className="site-collapse-custom-panel">
                                <p>{this.formatText("预示危险的自动信号发出的声音")}</p>
                            </Panel>
                            <Panel style={{whiteSpace: "pre-wrap"}} header="Mechanisms" key="Mechanisms"
                                   className="site-collapse-custom-panel">
                                <p>{this.formatText("源自人造机器和设备的声音")}</p>
                            </Panel>
                            <Panel style={{whiteSpace: "pre-wrap"}} header="Tools" key="Tools"
                                   className="site-collapse-custom-panel">
                                <p>{this.formatText("与可用于实现目标的任何物理物品相关的声音，特别是如果该物品在此过程中未被消耗")}</p>
                            </Panel>
                            <Panel style={{whiteSpace: "pre-wrap"}} header="Explosion" key="Explosion"
                                   className="site-collapse-custom-panel">
                                <p>{this.formatText("音量迅速增加并以极端方式释放能量的声音，通常伴随着高温的产生和气体的释放")}</p>
                            </Panel>
                            <Panel style={{whiteSpace: "pre-wrap"}} header="Wood" key="Wood"
                                   className="site-collapse-custom-panel">
                                <p>{this.formatText("与在树木和其他木本植物的茎和根中发现的多孔和纤维结构组织相关的声音")}</p>
                            </Panel>
                            <Panel style={{whiteSpace: "pre-wrap"}} header="Glass" key="Glass"
                                   className="site-collapse-custom-panel">
                                <p>{this.formatText("与非结晶无定形固体相关的声音，这种固体通常是透明的，具有广泛的实用、技术和装饰用途")}</p>
                            </Panel>
                            <Panel style={{whiteSpace: "pre-wrap"}} header="Liquid" key="Liquid"
                                   className="site-collapse-custom-panel">
                                <p>{this.formatText("符合其容器的形状，但保持恒定的体积，不受压力的影响的液体的声音")}</p>
                            </Panel>
                            <Panel style={{whiteSpace: "pre-wrap"}} header="Miscellaneous sources"
                                   key="Miscellaneous sources"
                                   className="site-collapse-custom-panel">
                                <p>{this.formatText("具体来源没有被其他类别所涵盖的声音类别")}</p>
                            </Panel>
                            <Panel style={{whiteSpace: "pre-wrap"}} header="Specific impact sounds"
                                   key="Specific impact sounds"
                                   className="site-collapse-custom-panel">
                                <p>{this.formatText("强烈暗示碰撞中涉及的特定物体的瞬态接触声音")}</p>
                            </Panel>
                        </Collapse>
                    </Panel>
                    <Panel style={{whiteSpace: "pre-wrap"}} header="Source-ambiguous sounds"
                           key="Source-ambiguous sounds"
                           className="site-collapse-custom-panel">
                        <p>{this.formatText("不会立即暗示特定源对象的声音，但更可能根据其声学特性被感知和描述")}</p>
                        <Collapse accordion bordered={false}
                                  expandIcon={({isActive}) => <CaretRightOutlined rotate={isActive ? 90 : 0}/>}>
                            <Panel style={{whiteSpace: "pre-wrap"}} header="Generic impact sounds"
                                   key="Generic impact sounds"
                                   className="site-collapse-custom-panel">
                                <p>{this.formatText("优先通过其声学特性而不是直接提及声源来描述的撞击或碰撞的声音")}</p>
                            </Panel>
                            <Panel style={{whiteSpace: "pre-wrap"}} header="Surface contact" key="Surface contact"
                                   className="site-collapse-custom-panel">
                                <p>{this.formatText("由两个对象或表面之间更广泛的交互产生的声音，而不是碰撞或反弹")}</p>
                            </Panel>
                            <Panel style={{whiteSpace: "pre-wrap"}} header="Deformable shell" key="Deformable shell"
                                   className="site-collapse-custom-panel">
                                <p>{this.formatText("与壳、刚性板或其他主要二维表面相关的声音")}</p>
                            </Panel>
                            <Panel style={{whiteSpace: "pre-wrap"}} header="Onomatopoeia" key="Onomatopoeia"
                                   className="site-collapse-custom-panel">
                                <p>{this.formatText("一类声音，命名为在语音上模仿、相似或暗示它所描述的声音")}</p>
                            </Panel>
                            <Panel style={{whiteSpace: "pre-wrap"}} header="Other sources" key="Other sources"
                                   className="site-collapse-custom-panel">
                                <p>{this.formatText("不由其他类别表示的一个声音类别，这些类别是由其声音而不是其来源感知的")}</p>
                            </Panel>
                        </Collapse>
                    </Panel>
                </Collapse>
            </Drawer>
        )
    }
}

export default PatternDrawer