import React from "react";
import {Cascader} from "antd";

class PatternDisplay extends React.Component {
    options = [
        {
            value: "Animal",
            label: "Animal",
            children: [
                {
                    value: "Pets",
                    label: "Pets",
                },
                {
                    value: "Livestock",
                    label: "Livestock",
                },
                {
                    value: "Wild animals",
                    label: "Wild animals",
                }
            ],
        },
        {
            value: "Gaussian noise",
            label: "Gaussian noise",
        },
        {
            value: "Human sounds",
            label: "Human sounds",
            children: [
                {
                    value: "Human voice",
                    label: "Human voice",
                },
                {
                    value: "Whistling",
                    label: "Whistling",
                },
                {
                    value: "Respiratory sounds",
                    label: "Respiratory sounds",
                },
                {
                    value: "Human locomotion",
                    label: "Human locomotion",
                },
                {
                    value: "Digestive",
                    label: "Digestive",
                },
                {
                    value: "Hands",
                    label: "Hands",
                },
                {
                    value: "Heartbeat",
                    label: "Heartbeat",
                },
                {
                    value: "Otoacoustic emission",
                    label: "Otoacoustic emission",
                },
                {
                    value: "Human group actions",
                    label: "Human group actions",
                }
            ],
        },
        {
            value: "Music",
            label: "Music",
            children: [
                {
                    value: "Musical instrument",
                    label: "Musical instrument",
                },
                {
                    value: "Music genre",
                    label: "Music genre",
                },
                {
                    value: "Musical concepts",
                    label: "Musical concepts",
                },
                {
                    value: "Music role",
                    label: "Music role",
                },
                {
                    value: "Music mood",
                    label: "Music mood",
                }
            ],
        },
        {
            value: "Natural sounds",
            label: "Natural sounds",
            children: [
                {
                    value: "Wind",
                    label: "Wind",
                },
                {
                    value: "Thunderstorm",
                    label: "Thunderstorm",
                },
                {
                    value: "Fire",
                    label: "Fire",
                },
                {
                    value: "Water",
                    label: "Water",
                },
            ],
        },
        {
            value: "Sound level",
            label: "Sound level",
            children: [
                {
                    value: "Louder",
                    label: "Louder",
                },
                {
                    value: "Quieter",
                    label: "Quieter",
                },
                {
                    value: "Pitch",
                    label: "Pitch",
                },
                {
                    value: "Speed",
                    label: "Speed",
                },
            ],
        },
        {
            value: "Sounds of things",
            label: "Sounds of things",
            children: [
                {
                    value: "Vehicle",
                    label: "Vehicle",
                },
                {
                    value: "Engine",
                    label: "Engine",
                },
                {
                    value: "Domestic sounds",
                    label: "Domestic sounds",
                },
                {
                    value: "Bell",
                    label: "Bell",
                },
                {
                    value: "Alarm",
                    label: "Alarm",
                },
                {
                    value: "Mechanisms",
                    label: "Mechanisms",
                },
                {
                    value: "Tools",
                    label: "Tools",
                },
                {
                    value: "Explosion",
                    label: "Explosion",
                },
                {
                    value: "Wood",
                    label: "Wood",
                },
                {
                    value: "Glass",
                    label: "Glass",
                },
                {
                    value: "Liquid",
                    label: "Liquid",
                },
                {
                    value: "Miscellaneous sources",
                    label: "Miscellaneous sources",
                },
                {
                    value: "Specific impact sounds",
                    label: "Specific impact sounds",
                },
            ],
        },
        {
            value: "Source-ambiguous sounds",
            label: "Source-ambiguous sounds",
            children: [
                {
                    value: "Generic impact sounds",
                    label: "Generic impact sounds",
                },
                {
                    value: "Surface contact",
                    label: "Surface contact",
                },
                {
                    value: "Deformable shell",
                    label: "Deformable shell",
                },
                {
                    value: "Onomatopoeia",
                    label: "Onomatopoeia",
                },
            ],
        }
    ];

    onChange = (value) => {
        const option = [];
        option.push(this.props.row)
        option.push(value)
        this.props.parent.getChildren(this, option)
    }

    render() {
        return (
            <Cascader style={{width: 330}} expandTrigger={"hover"} options={this.options} onChange={this.onChange}
                      placeholder="select the noise pattern"/>
        )
    }
}

export default PatternDisplay