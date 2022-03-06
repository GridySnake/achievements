import { Form, Input, Button, Checkbox } from 'antd';
import {Link} from "react-router-dom";
import {useNavigate} from "react-router";
import {useAuth} from "../hooks/AuthHooks";
import {login} from "../api/Auth";
import React, {useState} from "react";

const FormLogin = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [validationError, setValidationError] = useState(false);
    const {setUser, setAuthLoading} = useAuth();
    const navigate = useNavigate();

    const loginApp = () => {
        if (username === "") {
            setValidationError(true);
            return
        }
        setAuthLoading(true);
        login({email: username, password: password}, (data) => {
            if (data === null) {
                return
            }
            setUser(data);
            setAuthLoading(false);
            navigate(`/user/${data["user_id"]}`)
        })
    }

    const onPressSend = e => {
        if (e.key === "Enter" && username !== "") {
            loginApp();
        }

    }
  return (
    <Form
      name="basic"
      labelCol={{
        span: 6,
      }}
      wrapperCol={{
        span: 8,
      }}
      initialValues={{
        remember: false,
      }}
      autoComplete="off"
    >
      <Form.Item
        label="Username"
        name="username"
        rules={[
          {
            required: true,
            message: 'Username is required',
          },
        ]}
        onChange={e => setUsername(e.target.value)}
      >
        <Input />
      </Form.Item>

      <Form.Item
        label="Password"
        name="password"
        rules={[
          {
            required: true,
            message: 'Password is required',
          },
        ]}
        onChange={e => setPassword(e.target.value)}
        onKeyPress={e => onPressSend(e)}
      >
        <Input.Password />
      </Form.Item>

      <Form.Item
        name="remember"
        valuePropName="checked"
        wrapperCol={{
          offset: 8,
          span: 8,
        }}
      >
        <Checkbox>Remember me</Checkbox>
      </Form.Item>

      <Form.Item
        wrapperCol={{
          offset: 8,
          span: 8,
        }}
      >
        <Button type="primary" htmlType="button" onClick={() => loginApp()}>
                Sign In
        </Button>
      </Form.Item>
        {/*<Link to='/signup'>*/}
            <Button type="primary" htmlType="button" onClick={<Link to='/signup'/>}>
                Sign In
            </Button>
        {/*</Link>*/}
    </Form>
  )
}

export default FormLogin