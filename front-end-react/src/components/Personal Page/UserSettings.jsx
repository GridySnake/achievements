import React, {useEffect, useState} from "react";
import {Button, Form, Input, Select, DatePicker} from "antd";
import {GetAnyUserInfo, GetCitiesByCountry} from "../../api/GeneralApi";
import {ChangeUserSettings} from "../../api/SendForms";
import moment from "moment";

const UserSettings = () => {

    const { Option } = Select;

    const [PhoneNew, setPhoneNew] = useState(null);
    const [EmailNew, setEmailNew] = useState(null);
    const [NameNew, setNameNew] = useState(null);
    const [SurnameNew, setSurnameNew] = useState(null);
    const [UsernameNew, setUsernameNew] = useState(null);
    const [CountryNew, setCountryNew] = useState(null);
    const [CityNew, setCityNew] = useState(null);
    const [BioNew, setBioNew] = useState(null);
    const [ConditionsNew, setConditionsNew] = useState(null);
    const [BirthdayNew, setBirthdayNew] = useState(null);
    const [Show, setShow] = useState(false);
    const [Cities, setCities] = useState(null);
    const [Countries, setCountries] = useState(null);
    const [Data, setData] = useState({});
    const [Change, setChange] = useState(false);
    const NewData = {
        'phone': PhoneNew,
        'email': EmailNew,
        'name': NameNew,
        'surname': SurnameNew,
        'user_name': UsernameNew,
        'country_id': CountryNew,
        'city_id': CityNew,
        'bio': BioNew,
        'birthday': BirthdayNew
    }

    useEffect(() => {
        const UserInfo = (UserInfo) => {
            setData({
                'phone': UserInfo.user.phone,
                'email': UserInfo.user.email,
                'name': UserInfo.user.name,
                'surname': UserInfo.user.surname,
                'user_name': UserInfo.user.user_name,
                'country_id': UserInfo.user.country_id,
                'city_id': UserInfo.user.city_id,
                'bio': UserInfo.user.bio,
                'birthday': UserInfo.user.birthday
            })
            setPhoneNew(UserInfo.user.phone)
            setEmailNew(UserInfo.user.email)
            setNameNew(UserInfo.user.name)
            setSurnameNew(UserInfo.user.surname)
            setUsernameNew(UserInfo.user.user_name)
            setCountryNew(UserInfo.user.country_id)
            setCityNew(UserInfo.user.city_id)
            setBioNew(UserInfo.user.bio)
            setBirthdayNew(UserInfo.user.birthday)
            setCountries(UserInfo.countries)
            setCities(UserInfo.cities)
            setShow(true);
            }

        GetAnyUserInfo(UserInfo, '/user_info')
    }, [Change])

    useEffect(() => {
        const GetCities = (City) => {
            setCities(City.cities)
        }
        GetCitiesByCountry(CountryNew, GetCities)
    }, [CountryNew])

    const Reset = () => {
        setChange(true);
    }

    const SubmitChanges = () => {
        const SendValuesMain = {};
        const SendValuesInfo = {};
        const UserMain = ['user_name', 'phone', 'email'];
        for (const key in NewData) {
            if (NewData[key] !== Data[key]) {
                if (UserMain.includes(key)) {
                    SendValuesMain[key] = NewData[key]
                } else {
                    SendValuesInfo[key] = NewData[key]
                }
            }
        }
        console.log(SendValuesMain, SendValuesInfo)
        if (Object.keys(SendValuesMain).length !== 0) {
            SendValuesMain['table'] = 'user_main'
            ChangeUserSettings(SendValuesMain, (data) => {
            console.log(data)
            setChange(true);
            setChange(false);
        })
        }
        if (Object.keys(SendValuesInfo).length !== 0) {
            SendValuesInfo['table'] = 'user_info'
            ChangeUserSettings(SendValuesInfo, (data) => {
            console.log(data)
            setChange(true);
            setChange(false);
        })
        }
    }

    const isDisable = () => {
        return JSON.stringify(NewData) === JSON.stringify(Data);
    }

    return(
        Show?

        <Form>
            <Form.Item>
                <Input value={UsernameNew} onChange={e => setUsernameNew(e.target.value)}/>
            </Form.Item>
            <Form.Item>
                <Input.Password type="phone" value={PhoneNew} onChange={e => setPhoneNew(e.target.value)}/>
            </Form.Item>
            <Form.Item>
                <Input.Password type="email" value={EmailNew} onChange={e => setEmailNew(e.target.value)}/>
            </Form.Item>
            <Form.Item>
                <Input value={NameNew} onChange={e => setNameNew(e.target.value)}/>
            </Form.Item>
            <Form.Item>
                <Input value={SurnameNew} onChange={e => setSurnameNew(e.target.value)}/>
            </Form.Item>
            <Form.Item>
                <DatePicker value={moment(BirthdayNew)} onChange={date => setBirthdayNew(date.format("YYYY-MM-DD"))}/>
            </Form.Item>
            <Form.Item>
                <Select defaultValue={CountryNew} onChange={e => setCountryNew(e)}>
                    {Countries.map((country) => {
                        return (
                            <Option value={country.country_id}>{country.country_name}</Option>
                        )
                    })
                    }
                </Select>
            </Form.Item>
            {Cities?
                <Form.Item>
                    <Select defaultValue={CityNew} onChange={e => setCityNew(e)}>
                        {Cities.map((city) => {
                            return (
                                <Option value={city.city_id}>{city.city_name}</Option>
                            )
                        })
                        }
                    </Select>
                </Form.Item>
                :
                <></>
            }
            <Form.Item>
                <Input value={BioNew} onChange={e => setBioNew(e.target.value)}/>
            </Form.Item>
            <Button type="primary" disabled={isDisable()} onClick={SubmitChanges}>Submit</Button>
            <Button type="primary" disabled={isDisable()} onClick={Reset}>Reset</Button>
        </Form>
            :
            <></>
    )
}

export default UserSettings;