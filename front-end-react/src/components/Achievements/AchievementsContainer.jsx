import React, {useEffect, useState} from "react";
import {GetAnyUserInfo, GetSubspheresBySphere, GetConditionsByGroup, GetConditionsByService,
    GetConditionsByAggregation} from "../../api/GeneralApi";
import {Avatar, Button, Form, Input, List, Select, Skeleton, Tabs} from "antd";
import StaticAvatars from "../StaticRoutes";
import makeAction from "../../api/PageActions";
import {useNavigate} from "react-router";
import {Option} from "antd/es/mentions";

const { TabPane } = Tabs;

const AchievementsContainer = () => {
    const [Give, setGive] = useState(null);
    const [Get, setGet] = useState(null);
    const [Suggestions, setSuggestions] = useState(null);
    const [ToCreate, setToCreate] = useState(null);
    const [AchievementName, setAchievementName] = useState("");
    const [AchievementDescription, setAchievementDescription] = useState("");
    const [Group, setGroup] = useState("");
    const [Subsphere, setSubsphere] = useState("");
    const [Subspheres, setSubspheres] = useState("");
    const [Sphere, setSphere] = useState("");
    const [Service, setService] = useState("");
    const [Services, setServices] = useState("");
    const [Aggregation, setAggregation] = useState("");
    const [Aggregations, setAggregations] = useState("");
    const [Parameter, setParameter] = useState("");
    const [Parameters, setParameters] = useState("");
    const [Values, setValues] = useState("");
    const navigate = useNavigate();
    const url = '/achievements'

     useEffect(() => {
        const setInfoAchievements = (Achievements) => {
            setGive(Achievements.my)
            setGet(Achievements.get)
            setSuggestions(Achievements.suggestion)
            setToCreate(Achievements.create)

        }
        GetAnyUserInfo(setInfoAchievements, url)
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
        const GetConditionsByGroups = (Conditions) => {
            setServices(Conditions.services)
            setAggregations(Conditions.agg)
            setParameters(Conditions.parameters)
        }
        GetConditionsByGroup(Group, GetConditionsByGroups)
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
                </Form>
            </TabPane>
        </Tabs>
            </div>
            :
            <>1</>
    )
}

export default AchievementsContainer;