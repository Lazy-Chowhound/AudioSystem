import React from 'react';

class AudioPlay extends React.Component {
    render() {
        return (
            <div style={{flexDirection:"column", textAlign:"center"}}>
                <div>{this.props.name}</div>
                <audio
                    style={{height: 35, width: 300,marginTop:10}}
                    src={this.props.src}
                    controls={true}
                />
            </div>
        )
    }
}

export default AudioPlay