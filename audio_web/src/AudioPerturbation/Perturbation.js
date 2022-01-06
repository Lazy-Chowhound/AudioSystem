import React from 'react';
import 'antd/dist/antd.css';
import '../css/index.css';
import AudioPlay from "../AudioList/AudioPlay";

class Perturbation extends React.Component {
    render() {
        return (
            <AudioPlay name={"common_voice_zh-CN_18524189.mp3"}
                       src={"http://localhost:8080/Sound/common_voice_zh-CN_18524189.mp3"}/>
        );
    }
}

export default Perturbation
