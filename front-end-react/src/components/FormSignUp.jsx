import { Form, Input, Button, Checkbox, Radio } from 'antd';
import {useState, useEffect} from "react";

const FormSignUp = () => {

    const [EmailPhone, setEmailPhone] = useState('email')
    // const EmailPhoneCheck = (check) => {
    //     useEffect(() => {
    //         setEmailPhone(check)
    //     }
    //     )
    // }
    // const [CheckEmailPhone, setCheck] = useState({
    //     'email': true,
    //     'phone': false})
    // const EmailPhoneCheck = (Check) => {
    //     if (Check === 'phone') {
    //         setCheck({'email': false, 'phone': true})
    //     } else {
    //         setCheck({'email': true, 'phone': false})
    //         }
    // }
    // const CheckEmailPhone = EmailPhoneCheck(Check)
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
            wrapperCol={{
                offset: 8,
                span: 8,
            }}
        >
            <Radio.Group value={EmailPhone} onChange={(check) => setEmailPhone(check.target.value)}>
                <Radio.Button value={'email'} key={'email'}>Email</Radio.Button>
                <Radio.Button value={'phone'} key={'phone'}>Phone</Radio.Button>
            </Radio.Group>
        </Form.Item>
      <Form.Item
        label={EmailPhone.charAt(0).toUpperCase() + EmailPhone.slice(1)}
        name={EmailPhone}
        rules={[
          {
            required: true,
            message: EmailPhone + ' is required',
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
          Sign Up
        </Button>
      </Form.Item>
    </Form>
  )
}

export default FormSignUp