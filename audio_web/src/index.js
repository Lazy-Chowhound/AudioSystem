import React from "react";
import ReactDOM from "react-dom";
import {Breadcrumb, Button, Form, Input, Layout, Menu, message, Modal} from "antd";
import {
    BarsOutlined, BarChartOutlined,
    PullRequestOutlined, SlidersOutlined, ControlOutlined
} from "@ant-design/icons";
import {BrowserRouter as Router, Link, Route, Routes} from "react-router-dom";
import AudioList from "./AudioList/AudioList";
import PerturbationDisplay from "./AudioPerturbationDisplay/PerturbationDisplay";
import Validation from "./AudioValidation/Validation";

import "./css/index.css";
import PerturbationAttach from "./AudioPerturbationAttach/PerturbationAttach";
import {sendGet} from "./Util/axios";

const {Header, Content, Footer, Sider} = Layout;
const {SubMenu} = Menu;

class Index extends React.Component {
    state = {
        collapsed: false,
        selectedPath: ["list"],
        choice: "音频列表",
        subChoice: "",
        openKeys: [],
        isLogin: false,
        registerModal: false,
        loginModal: false,
        registerForm: React.createRef(),
        loginForm: React.createRef(),
        userName: null
    };

    componentDidMount() {
        const token = localStorage.getItem("token")
        sendGet("/verifyToken", {
            params: {
                token: token
            }
        }).then(res => {
            if (res.data.code === 400) {
                message.warn(res.data.data).then()
            } else {
                const data = res.data.data.split(" ");
                const token = data[0];
                const userName = data[1];
                this.setState({
                    isLogin: true,
                    userName: userName
                })
                localStorage.setItem("token", token);
            }
        }).catch(err => {
            message.error(err).then()
        })
        this.changeSelectedKeys()
    }

    onCollapse = (collapsed) => {
        this.setState({collapsed});
    };

    handleClick = (e) => {
        if (e.key === "title") {
            return;
        }
        this.changeSelectedKeys()
    };

    changeSelectedKeys = () => {
        const menu = new Map([["list", "音频列表"], ["noise", "音频扰动"], ["validation", "质量分析"]])
        const submenu = new Map([["perturbationAttach", "添加扰动"], ["perturbationDisplay", "扰动概况"]])
        let curPath = []
        let path = new URL(window.location.href).pathname
        if (path === "/") {
            curPath.push("list")
        } else {
            if (path === "/perturbationAttach" || path === "/perturbationDisplay") {
                curPath.push("noise")
            }
            curPath.push(path.substring(1))
        }
        this.setState({
            selectedPath: curPath,
            openKeys: curPath.length === 2 ? ["noise"] : [],
            choice: menu.get(curPath[0]),
            subChoice: curPath.length === 2 ? submenu.get(curPath[1]) : null
        })
    }

    handleOpenChange = () => {
        this.setState({
            openKeys: ["noise"]
        })
    }

    showRegister = () => {
        this.setState({
            registerModal: true
        })
    }

    cancelRegister = () => {
        this.setState({
            registerModal: false
        })
    }

    showLogin = () => {
        this.setState({
            loginModal: true
        })
    }

    cancelLogin = () => {
        this.setState({
            loginModal: false
        })
    }

    checkRepeatPassword = () => {
        const password = this.state.registerForm.current.getFieldsValue().password;
        const rePassword = this.state.registerForm.current.getFieldsValue().repeatPassword;
        if (password !== rePassword) {
            return Promise.reject("两次密码不一致")
        }
        return Promise.resolve();
    }

    register = (values) => {
        sendGet("/register", {
            params: {
                userName: values['userName'],
                password: values['password']
            }
        }).then(res => {
            if (res.data.code === 200) {
                message.success("注册成功，请登录").then()
                this.setState({
                    registerModal: false
                })
                this.state.registerForm.current.resetFields();
            } else {
                message.warn(res.data.data).then()
            }
        }).catch(() => {
            message.error("注册失败").then()
        })
    }

    login = (values) => {
        sendGet("/login", {
            params: {
                userName: values['userName'],
                password: values['password']
            }
        }).then(res => {
            if (res.data.code === 200) {
                message.success("登录成功").then()
                this.setState({
                    isLogin: true,
                    loginModal: false,
                    userName: values['userName']
                })
                this.state.loginForm.current.resetFields();
                //保存token
                const token = res.data.data
                localStorage.setItem("token", token);
                window.location.reload()
            } else {
                message.warn(res.data.data).then()
            }
        }).catch(() => {
            message.error("登录失败").then()
        })
    }

    logout = () => {
        sendGet("/logout").then(() => {
            message.success("成功登出").then()
            this.setState({
                isLogin: false
            })
            //清除token
            localStorage.removeItem("token")
            window.location.reload()
        }).catch(() => {
            message.error("登出失败").then()
        })
    }

    render() {
        const {collapsed} = this.state;

        let header;
        if (!this.state.isLogin) {
            header = <div style={{textAlign: "right"}}>
                <Button onClick={this.showLogin} style={{marginRight: "20px"}} type={"primary"}>登录</Button>
                <Button onClick={this.showRegister} style={{marginRight: "20px"}} type={"primary"}>注册</Button>
            </div>
        } else {
            header = <div style={{textAlign: "right"}}>
                <span style={{marginRight: "20px"}}>当前用户：{this.state.userName}</span>
                <Button onClick={this.logout} style={{marginRight: "20px"}} type={"primary"}>登出</Button>
            </div>
        }
        return (
            <Router>
                <Layout style={{minHeight: "100vh"}}>
                    <Sider collapsible collapsed={collapsed} onCollapse={this.onCollapse}>
                        <Menu theme="dark" mode="inline" onClick={this.handleClick}
                              selectedKeys={this.state.selectedPath}
                              openKeys={this.state.openKeys}
                              onOpenChange={this.handleOpenChange}>
                            <Menu.Item className="title" key="title">
                                音频数据集系统
                            </Menu.Item>
                            <Menu.Item key="list" icon={<BarsOutlined/>}>
                                <Link to={"/list"}>音频列表</Link>
                            </Menu.Item>
                            <SubMenu key="noise" icon={<SlidersOutlined/>} title={"音频扰动"}>
                                <Menu.Item key="perturbationAttach" icon={<PullRequestOutlined/>}>
                                    <Link to={"/perturbationAttach"}>添加扰动</Link>
                                </Menu.Item>
                                <Menu.Item key="perturbationDisplay" icon={<BarChartOutlined/>}>
                                    <Link to={"/perturbationDisplay"}>扰动概况</Link>
                                </Menu.Item>
                            </SubMenu>
                            <Menu.Item key="validation" icon={<ControlOutlined/>}>
                                <Link to={"/validation"}>质量分析</Link>
                            </Menu.Item>
                        </Menu>
                    </Sider>
                    <Layout className="site-layout">
                        <Header className="site-layout-background" style={{padding: 0}}>
                            {header}
                        </Header>
                        <Content style={{margin: "0 16px"}}>
                            <Breadcrumb style={{margin: "16px 0"}}>
                                <Breadcrumb.Item>音频数据集系统</Breadcrumb.Item>
                                <Breadcrumb.Item>{this.state.choice}</Breadcrumb.Item>
                                <Breadcrumb.Item>{this.state.subChoice}</Breadcrumb.Item>
                            </Breadcrumb>
                            <div className="site-layout-background" style={{minHeight: 400}}>
                                <Routes>
                                    <Route exact path="/" element={<AudioList key={this.state.isLogin}/>}/>
                                    <Route exact path="/list" element={<AudioList key={this.state.isLogin}/>}/>
                                    <Route exact path="/perturbationAttach" element={<PerturbationAttach/>}/>
                                    <Route exact path="/perturbationDisplay" element={<PerturbationDisplay/>}/>
                                    <Route exact path="/validation" element={<Validation/>}/>
                                </Routes>
                            </div>
                        </Content>
                        <Footer style={{textAlign: "center"}}>Audio System ©2022 Created by Nakano Miku</Footer>
                    </Layout>
                </Layout>
                <Modal visible={this.state.registerModal} footer={null} title={"注册"} onCancel={this.cancelRegister}>
                    <Form ref={this.state.registerForm} name="registerForm" labelCol={{span: 8}} wrapperCol={{span: 16}}
                          onFinish={this.register} labelAlign={"left"} autoComplete="off">
                        <Form.Item label="用户名" name="userName" rules={[{required: true, message: "请输入用户名称"}]}>
                            <Input/>
                        </Form.Item>
                        <Form.Item label="密码" name="password" rules={[{required: true, message: "请输入密码"}]}>
                            <Input.Password/>
                        </Form.Item>
                        <Form.Item label="再次输入密码" name="repeatPassword"
                                   rules={[{required: true, message: ""}, {validator: this.checkRepeatPassword}]}>
                            <Input.Password/>
                        </Form.Item>
                        <Form.Item wrapperCol={{offset: 8, span: 16}}>
                            <Button type="primary" htmlType="submit">注册</Button>
                        </Form.Item>
                    </Form>
                </Modal>
                <Modal visible={this.state.loginModal} footer={null} title={"登录"} onCancel={this.cancelLogin}>
                    <Form ref={this.state.loginForm} name="loginForm" labelCol={{span: 8}} wrapperCol={{span: 16}}
                          onFinish={this.login} labelAlign={"left"} autoComplete="off">
                        <Form.Item label="用户名" name="userName"
                                   rules={[{required: true, message: "请输入用户名称"}]}>
                            <Input/>
                        </Form.Item>
                        <Form.Item label="密码" name="password"
                                   rules={[{required: true, message: "请输入密码"}]}>
                            <Input.Password/>
                        </Form.Item>
                        <Form.Item wrapperCol={{offset: 8, span: 16}}>
                            <Button type="primary" htmlType="submit">登录</Button>
                        </Form.Item>
                    </Form>
                </Modal>
            </Router>
        );
    }
}

ReactDOM.render(<Index/>, document.getElementById("root"));
