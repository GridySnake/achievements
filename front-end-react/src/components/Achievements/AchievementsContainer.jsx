import React, {useEffect, useState, useRef} from "react";
import {GetAnyInfo, GetSubspheresBySphere, GetConditionsByGroup, GetConditionsByService,
    GetConditionsByAggregation, GetUsersByType} from "../../api/GeneralApi";
import {Avatar, Button, Form, Input, List, Select, Skeleton, Tabs, DatePicker} from "antd";
import {CreateAchievement} from "../../api/SendForms";
import moment from "moment";
import StaticAvatars from "../StaticRoutes";
import type { RadioChangeEvent } from 'antd';
import { Radio } from 'antd';
import makeAction from "../../api/PageActions";
import {useNavigate} from "react-router";
import {Option} from "antd/es/mentions";
import { YMaps, Map, Placemark, SearchControl } from "react-yandex-maps";
const { RangePicker } = DatePicker;
const { TabPane } = Tabs;

const AchievementsContainer = () => {
    const [Give, setGive] = useState(null);
    const [Get, setGet] = useState(null);
    const [Suggestions, setSuggestions] = useState(null);
    const [ToCreate, setToCreate] = useState(null);
    const [AchievementName, setAchievementName] = useState(null);
    const [AchievementDescription, setAchievementDescription] = useState(null);
    const [Group, setGroup] = useState(null);
    const [Answer, setAnswer] = useState(null);
    const [Answers, setAnswers] = useState(null);
    const [Subsphere, setSubsphere] = useState(null);
    const [Subspheres, setSubspheres] = useState(null);
    const [Sphere, setSphere] = useState(null);
    const [Service, setService] = useState(null);
    const [Services, setServices] = useState(null);
    const [Aggregation, setAggregation] = useState(null);
    const [Aggregations, setAggregations] = useState(null);
    const [Parameter, setParameter] = useState(null);
    const [Parameters, setParameters] = useState(null);
    const [Values, setValues] = useState(null);
    const [UserType, setUserType] = useState(null);
    const [UserId, setUserId] = useState(null);
    const [Users, setUsers] = useState(null);
    const [Test, setTest] = useState(null);
    const [Dates, setDates] = useState([null, null]);
    const [coords, setCoords] = useState([null, null]);
    const [text, setText] = useState(null);
    const [mapCondition, setMapCondition] = useState(false);
    const navigate = useNavigate();
    const searchRef = useRef(null);

    const url = '/achievements'
    const RadioOptions = [
      {label: 'User', value: 0},
      {label: 'Community', value: 1},
      {label: 'Course', value: 2},
    ];
    const avatarPath = {0: StaticAvatars.StaticAvatars, 1: StaticAvatars.StaticGroupAvatars,
        2: StaticAvatars.StaticCommunityAvatars, 3: StaticAvatars.StaticCourseAvatars}

     useEffect(() => {
        const setInfoAchievements = (Achievements) => {
            setGive(Achievements.my)
            setGet(Achievements.get)
            setSuggestions(Achievements.suggestion)
            setToCreate(Achievements.create)
        }
        GetAnyInfo(setInfoAchievements, url)
    }, [url])

    const HideShow = (item) => {
        if (item.item.hide_achievements === 0) {
            return (
                <Button type="primary" htmlType="button" onClick={() => Hide(item.item.achievement_id)}>Hide</Button>
            )
        } else if (item.item.hide_achievements === 1) {
            return (
                <Button type="primary" htmlType="button" onClick={() => Show(item.item.achievement_id)}>Show</Button>
            )
        } else {
            return (<></>)
        }
    }

    const Show = (item) => {
        console.log(item)
        makeAction('/show_achievement', {'achievement_id': item, 'user_type': 0}, (value) => {
            setGet(value)
        })
    }

    const Hide = (item) => {
         makeAction('/hide_achievement', {'achievement_id': item, 'user_type': 0}, (value) => {
            setGet(value)
        })
    }

    const Delete = (item) => {
        makeAction('/drop_achievement', {'achievement_id': item, 'user_type': 0}, (value) => {
            setGive(value)
        })
    }

    const Goal = (item) => {
        makeAction('/desire', {'achievement_id': item, 'user_type': 0}, (value) => {
            setGive(value)
        })
    }

    useEffect(() => {
        const GetSubspheres = (Subspheres) => {
            setSubspheres(Subspheres.subspheres)
        }
        GetSubspheresBySphere(Sphere, GetSubspheres)
    }, [Sphere])

    useEffect(() => {
        if (Group !== 8) {
            const GetConditionsByGroups = (Conditions) => {
                setServices(Conditions.services)
                setAggregations(Conditions.agg)
                setParameters(Conditions.parameters)
                if (Group === 6) {
                    setAnswers(true)
                } else {
                    setAnswers(false)
                }
            }
            GetConditionsByGroup(Group, GetConditionsByGroups)
        }
    }, [Group])

    useEffect(() => {
        const GetConditionsByServices = (Conditions) => {
            setAggregations(Conditions.agg)
            setParameters(Conditions.parameters)
        }
        GetConditionsByService(Service, GetConditionsByServices)
    }, [Service])

    useEffect(() => {
        const GetConditionsByAggregations = (Conditions) => {
            setParameters(Conditions.parameters)
        }
        GetConditionsByAggregation(`${Group}_${Service}_${Aggregation}`, GetConditionsByAggregations)
    }, [Aggregation, Service])

    useEffect(() => {
        if (UserType !== 0) {
            const GetUsersByTypes = (User) => {
                setUsers(User.users)
            }
            GetUsersByType(UserType, GetUsersByTypes)
        } else {
            setUsers(null)
            setUserId(null)
        }
    }, [UserType])

    const RadioChange = ({ target: { value } }: RadioChangeEvent) => {
        setUserType(value);
    };

    // useEffect(() => {
    // if (text && searchRef.current) {
    //   searchRef.current.search(text);
    //     }
    // }, [text]);

    useEffect(() => {
        if (Aggregation) {
            if (Group === 2 && parseInt(Aggregation) === 1) {
                setMapCondition(true)
            } else {
                setMapCondition(false)
            }
        } else {
            setMapCondition(false)
        }
    }, [Group, Aggregation])

    const CreateAchievements = () => {
        const send = {'name': AchievementName, 'description':AchievementDescription, 'user_type': UserType,
            'user_id': UserId, 'select_parameter': Parameter, 'value': Values, 'test_url': Test, 'answer_url': Answer,
            'select_subsphere': Subsphere, 'dates': Dates}
        CreateAchievement(send, (data) => {
            navigate(`/achievement/${data}`)
        })
    };

    console.log(Group, Aggregation)

    return (
        ToCreate?
            <div>
                <Tabs defaultActiveKey="Suggestions">
                    <TabPane tab="Suggestions" key="Suggestions">
                        <List
                            itemLayout="horizontal"
                            dataSource={Suggestions}
                            renderItem={item => (
                                <List.Item>
                                    <Skeleton title={false} loading={item.loading} active>
                                        <List.Item.Meta
                                            title={<a href={'/achievement/' + item.achievement_id}>{item.title}</a>}
                                            description={item.description}
                                        />
                                    </Skeleton>
                                    <Button type="primary" htmlType="button" onClick={() => Goal(item.achievement_id)}>Set goal</Button>
                                </List.Item>
                            )}
                        />
                    </TabPane>
                    <TabPane tab="Created" key="Created">
                        <List
                            itemLayout="horizontal"
                            dataSource={Give}
                            renderItem={item => (
                                <List.Item>
                                    <Skeleton title={false} loading={item.loading} active>
                                        <List.Item.Meta
                                            title={<a href={'/achievement/' + item.achievement_id}>{item.name}</a>}
                                            description={item.description}
                                        />
                                        <Button type="primary" htmlType="button" onClick={() => Delete(item.achievement_id)}>Delete</Button>
                                    </Skeleton>
                                </List.Item>
                            )}
                        />
            </TabPane>
            <TabPane tab="Received" key="Received">
                <List
                    itemLayout="horizontal"
                    dataSource={Get}
                    renderItem={item => (
                        <List.Item>
                            <Skeleton title={false} loading={item.loading} active>
                                <List.Item.Meta
                                    title={<a href={'/achievement/' + item.achievement_id}>{item.name}</a>}
                                    description={item.description}
                                />
                                <HideShow item={item}/>
                            </Skeleton>
                        </List.Item>
                    )}
                />
            </TabPane>
            <TabPane tab="Create" key="Create">
                <Form name="create achievement"
                      labelCol={{
                        span: 6,
                      }}
                      wrapperCol={{
                        span: 8,
                      }}>
                    <Form.Item
                        label="Achievement name"
                        name="achievement_name"
                        rules={[
                          {
                            required: true,
                            message: 'Achievement name is required',
                          },
                        ]}
                        onChange={e => setAchievementName(e.target.value)}
                    >
                        <Input />
                    </Form.Item>
                    <Form.Item
                        label="Achievement description"
                        name="achievement_description"
                        rules={[
                          {
                            required: true,
                            message: 'Achievement description is required',
                          },
                        ]}
                        onChange={e => setAchievementDescription(e.target.value)}
                    >
                        <Input />
                    </Form.Item>
                    <Form.Item
                        label="Achievement creator type"
                        name="achievement_creator_type"
                        rules={[
                          {
                            required: true,
                            message: 'Achievement creator type is required',
                          }
                        ]}>
                        <Radio.Group
                            options={RadioOptions}
                            onChange={RadioChange}
                            value={null}
                            optionType="button"
                            buttonStyle="solid"
                          />
                    </Form.Item>
                    {Users?
                        <Form.Item
                            label="Achievement creator"
                            name="achievement_creator"
                            rules={[
                              {
                                required: true,
                                message: 'Achievement creator is required',
                              }
                            ]}>
                            <Select defaultValue={null} onChange={e => setUserId(e)}>
                                {Users.map((user) => {
                                    return (
                                        <Option value={user.user_id}><Avatar src={avatarPath[UserType+1] + user.href}/>
                                            {user.user_name}</Option>
                                    )
                                })
                                }
                            </Select>
                        </Form.Item>
                        :
                        <></>
                    }
                    <Form.Item
                        label="Achievement sphere"
                        name="achievement_sphere"
                        rules={[
                          {
                            required: true,
                            message: 'Achievement sphere is required',
                          }
                        ]}>
                        <Select defaultValue={null} onChange={e => setSphere(e)}>
                            {ToCreate.spheres.map((sphere) => {
                                return (
                                    <Option value={sphere.sphere_id}>{sphere.sphere_name}</Option>
                                )
                            })
                            }
                        </Select>
                    </Form.Item>
                    {Subspheres?
                        <Form.Item
                            label="Achievement subsphere"
                            name="achievement_subsphere"
                            rules={[
                              {
                                required: true,
                                message: 'Achievement subsphere is required',
                              }
                            ]}>
                            <Select defaultValue={null} onChange={e => setSubsphere(e)}>
                                {Subspheres.map((subsphere) => {
                                    return (
                                        <Option value={subsphere.subsphere_id}>{subsphere.subsphere_name}</Option>
                                    )
                                })
                                }
                            </Select>
                        </Form.Item>
                        :
                        <></>
                    }
                    <Form.Item
                        label="Achievement group"
                        name="achievement_group"
                        rules={[
                          {
                            required: true,
                            message: 'Achievement group is required',
                          }
                        ]}>
                        <Select defaultValue={null} onChange={e => setGroup(e)}>
                            {ToCreate.groups.map((group) => {
                                return (
                                    <Option value={group.group_id}>{group.group_name}</Option>
                                )
                            })
                            }
                        </Select>
                    </Form.Item>
                    {Services ?
                        <Form.Item
                            label="Achievement service"
                            name="achievement_service"
                            rules={[
                                {
                                    required: true,
                                    message: 'Achievement service is required',
                                }
                            ]}>
                            <Select defaultValue={null} onChange={e => setService(e)}>
                                {Services.map((service) => {
                                    return (
                                        <Option value={service.service_id}>{service.service_name}</Option>
                                    )
                                })
                                }
                            </Select>
                        </Form.Item>
                        :
                        <></>
                    }
                    {Aggregations?
                        <Form.Item
                            label="Achievement aggregation"
                            name="achievement_aggregation"
                            rules={[
                              {
                                required: true,
                                message: 'Achievement aggregation is required',
                              }
                            ]}>
                            <Select defaultValue={null} onChange={e => setAggregation(e)}>
                                {Aggregations.map((aggregation) => {
                                    return (
                                        <Option value={aggregation.aggregate_id}>{aggregation.aggregate_name}</Option>
                                    )
                                })
                                }
                            </Select>
                        </Form.Item>
                        :
                        <></>
                    }
                    {Parameters?
                        <Form.Item
                            label="Achievement parameter"
                            name="achievement_parameter"
                            rules={[
                              {
                                required: true,
                                message: 'Achievement parameter is required',
                              }
                            ]}>
                            <Select defaultValue={null} onChange={e => setParameter(e)}>
                                {Parameters.map((parameter) => {
                                    return (
                                        <Option value={parameter.parameter_id}>{parameter.parameter_name}</Option>
                                    )
                                })
                                }
                            </Select>
                        </Form.Item>
                        :
                        <></>
                    }
                    {/*{mapCondition?*/}
                    {/*    // <YMaps>*/}
                    {/*    //     <div>*/}
                    {/*    //         <Map*/}
                                    // onClick={e => setCoords(e._sourceEvent.originalEvent.coords)}
                                // >
                                    {/*<SearchControl*/}
                                    {/*    instanceRef={(ref) => {*/}
                                    {/*      if (ref) searchRef.current = ref;*/}
                                    {/*    }}*/}
                                    {/*    options={{*/}
                                    {/*      float: "right",*/}
                                    {/*      provider: "yandex#search",*/}
                                    {/*      size: "large"*/}
                                    {/*    }}*/}
                                    {/*/>*/}
                    {/*                {coords?*/}
                    {/*                    <Placemark*/}
                    {/*                    geometry={coords}*/}
                    {/*                    />*/}
                    {/*                    :*/}
                    {/*                    <></>*/}
                    {/*                }*/}
                    {/*//             </Map>*/}
                    {/*//         </div>*/}
                    {/*//     </YMaps>*/}
                    {/*//     :*/}
                    {/*//     <></>*/}
                    {/*// }*/}
                    {Answers?
                        <Form.Item
                            label="Achievement test"
                            name="achievement_test"
                            rules={[
                                {
                                    required: true,
                                    message: 'Achievement test is required',
                                },
                            ]}
                            onChange={e => setTest(e.target.value)}
                        >
                            <Input/>
                        </Form.Item>
                        :
                        <></>
                    }
                    {Answers?
                        <Form.Item
                            label="Achievement answer"
                            name="achievement_answer"
                            rules={[
                                {
                                    required: true,
                                    message: 'Achievement answer is required',
                                },
                            ]}
                            onChange={e => setAnswer(e.target.value)}
                        >
                            <Input/>
                        </Form.Item>
                        :
                        <></>
                    }
                    {Parameters ?
                        <Form.Item
                            label="Achievement value"
                            name="achievement_value"
                            rules={[
                                {
                                    required: true,
                                    message: 'Achievement value is required',
                                },
                            ]}
                            onChange={e => setValues(e.target.value)}
                        >
                            <Input/>
                        </Form.Item>
                        :
                        <></>
                    }
                    <Form.Item label="Achievement dates"
                            name="achievement_dates"
                            onChange={date => setDates(date.format("YYYY-MM-DD"))}
                        >
                        <RangePicker format={'YYYY-MM-DD'} onChange={dates => setDates(dates)} disabledDate={current => {
                            return current && current <= moment().subtract(1, 'days')}
                        }/>
                    </Form.Item>
                    <Button type="primary" onClick={CreateAchievements}>Create Achievement</Button>
                </Form>
            </TabPane>
        </Tabs>
            </div>
            :
            <>1</>
    )
}

export default AchievementsContainer;