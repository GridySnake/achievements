import { Form, Input, Button, Checkbox } from 'antd';
// import {useState} from "react";

const FormLogin = () => {
    // const [username, setUsername] = useState("");
    // const [validationError, setValidationError] = useState(false);
    // const {setUser, setAuthLoading} = useAuth();
    //
    // const loginApp = () => {
    //     if (username === "") {
    //         setValidationError(true);
    //         return
    //     }
    //     setAuthLoading(true);
    //     login({user_name: username}, setUser, () => {
    //         setAuthLoading(false);
    //     })
    // }
    const onFinish = (values) => {
    console.log('Success:', values);
  };

  const onFinishFailed = (errorInfo) => {
    console.log('Failed:', errorInfo);
  };
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
      onFinish={onFinish}
      onFinishFailed={onFinishFailed}
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
        <Button type="primary" htmlType="submit">
          Submit
        </Button>
      </Form.Item>
    </Form>
  )
}

export default FormLogin