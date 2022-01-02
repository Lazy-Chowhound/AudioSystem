import React from 'react';
import ReactDOM from 'react-dom';
import 'antd/dist/antd.css';
import './index.css';
import {Breadcrumb, Layout, Menu} from 'antd';
import {AudioOutlined, BarsOutlined, FireOutlined} from "@ant-design/icons";
import {BrowserRouter as Router, Link, Route, Routes} from "react-router-dom";
import AudioList from "./AudioList";
import Perturbation from "./Perturbation";
import Validation from "./Validation";

const {Header, Content, Footer, Sider} = Layout;

class SiderDemo extends React.Component {
    state = {
        collapsed: false,
        choice: "音频列表",
    };

    onCollapse = collapsed => {
        this.setState({collapsed});
    };

    handleClick = e => {
        if (e.key === "title") {
            return;
        }
        if (e.key === "list") {
            this.setState({
                choice: "音频列表"
            })
        } else if (e.key === "noise") {
            this.setState({
                choice: "音频扰动"
            })
        } else if (e.key === "evaluation") {
            this.setState({
                choice: "质量分析"
            })
        }
    };

    render() {
        const {collapsed} = this.state;
        return (
            <Router>
                <Layout style={{minHeight: '100vh'}}>
                    <Sider collapsible collapsed={collapsed} onCollapse={this.onCollapse}>
                        <Menu theme="dark" className="menu" onClick={this.handleClick} defaultSelectedKeys={["list"]}
                              mode="inline">
                            <Menu.Item className="title" key="title">
                                音频数据集系统
                            </Menu.Item>
                            <Menu.Item key="list" icon={<BarsOutlined/>}>
                                <Link to={"/list"}>音频列表</Link>
                            </Menu.Item>
                            <Menu.Item key="noise" icon={<AudioOutlined/>}>
                                <Link to={"/perturbation"}>音频扰动</Link>
                            </Menu.Item>
                            <Menu.Item key="evaluation" icon={<FireOutlined/>}>
                                <Link to={"/validation"}>质量分析</Link>
                            </Menu.Item>
                        </Menu>

                    </Sider>
                    <Layout className="site-layout">
                        <Header className="site-layout-background" style={{padding: 0}}/>
                        <Content style={{margin: '0 16px'}}>
                            <Breadcrumb style={{margin: '16px 0'}}>
                                <Breadcrumb.Item>音频数据集系统 </Breadcrumb.Item>
                                <Breadcrumb.Item>{this.state.choice}</Breadcrumb.Item>
                            </Breadcrumb>
                            <div className="site-layout-background" style={{padding: 24, minHeight: 360}}>
                                <Routes>
                                    <Route exact path="/" element={<AudioList/>}/>
                                    <Route exact path="/list" element={<AudioList/>}/>
                                    <Route exact path="/perturbation" element={<Perturbation/>}/>
                                    <Route exact path="/validation" element={<Validation/>}/>
                                </Routes>
                            </div>
                        </Content>
                        <Footer style={{textAlign: 'center'}}>Audio System ©2022 Created by Nakano Miku</Footer>
                    </Layout>
                </Layout>
            </Router>
        );
    }
}

ReactDOM.render(<SiderDemo/>, document.getElementById("root"));
