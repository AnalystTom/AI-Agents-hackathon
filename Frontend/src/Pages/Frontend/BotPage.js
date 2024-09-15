import React, { useState, useRef, useEffect } from 'react';
import userImg from '../../Assets/user.png';
import bot from "../../Assets/bot.png";
import ResponseLoader from 'Components/Screen Loader/ResponseLoader';
// ------------- Laptop Images ---------------------
import laptop1 from "../../Assets/laptop1.png"
import laptop2 from "../../Assets/laptop2.png"
import laptop3 from "../../Assets/laptop3.png"
import { message } from 'antd';

export default function BotPage() {

    const [products, setProducts] = useState([]);
    const [state, setState] = useState({ text: "" });
    const [messages, setMessages] = useState([]);
    const [loader, setLoader] = useState(false);
    const dummy = useRef();


    let uid = Math.random().toString().slice(2, 15);

    const handleChange = (e) => setState({ ...state, [e.target.name]: e.target.value });
    const handleSubmit = async () => {
        if (!state.text) {
            message.warning("Enter Prompt")
            return;
        }
        setLoader(true);
        setMessages(prevMessages => [...prevMessages, { message: state.text, uid }]);


        try {
            const response = await fetch('https://fakestoreapi.com/products?limit=3');
            const result = await response.json();
            setProducts(result);
            console.log(result)
            setMessages(prevMessages => [...prevMessages, result]);
        } catch (error) {
            console.error('Error fetching prediction:', error);
        }
        setState({ text: "" });
        setLoader(false);


    };


    const handleFocus = () => {
        document.getElementById("text").style.outline = "none";
    };

    // Submit on Enter key

    const handleKeyPress = (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSubmit();
        }
    };

    // For smooth scroll

    useEffect(() => {
        dummy.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    return (
        <main className='bot-page'>
            <h2 className="text-start text-light my-3 mx-3">
                Product Recommender
            </h2>
            <div className="container-fluid chatContaienr" style={{ "minHeight": "75vh" }}>
                {/* <h1 className="text-center text-white my-4" id='assisttext'>
                    How can I assist you with Product Recomendation?
                </h1> */}
                {messages.map((message, i) => {
                    const className = message.uid ? "userMessage" : "botMessage";
                    const margin = message.uid ? "ms-auto me-4" : "me-auto ms-4 mb-4";
                    const text = message.uid ? "text-start" : "text-start";
                    const img = message.uid ? userImg : "";
                    const width = message.uid ? "50px" : "90px";
                    return (
                        <div className={`${className} ${text} mt-4 ${margin}`} key={i}>
                            {message.uid
                                ?
                                <img src={userImg} style={{ width, height: "55px", borderRadius: "50%", margin: "0px 17px" }} alt="" />
                                :
                                <></>}

                            {/* User message */}
                            <div className="container">
                                <div className="row ">
                                    {typeof message === 'object' && !Array.isArray(message) ? (
                                        <>
                                            {
                                                message.uid
                                                    ?
                                                    <div className="col-12 p-0">
                                                        <p className="m-0 ms-auto userInput" id='userInput'>
                                                            {message.message}
                                                        </p>
                                                    </div>
                                                    :
                                                    <div className="col-12 p-0">
                                                        <p className="m-0 me-auto output" id='output'>
                                                            {message.message}
                                                        </p>
                                                    </div>
                                            }
                                        </>
                                    ) : (
                                        message.map((product, idx) => {
                                            return (
                                                <div className="col-12 col-md-6 col-lg-4 my-3">
                                                    <div className="product-card" key={product.id}>
                                                        <h3>{product.title}</h3>
                                                        <h6 className='my-3'><b>Category:- </b>{product.category}</h6>
                                                        <img src={product.image} alt="" />
                                                        <div className="my-4 d-flex justify-content-between align-items-center">
                                                            <p className='m-0'>${product.price}</p>
                                                            {product.rating && (
                                                                <div className="rating">
                                                                    <p className='m-0 d-flex flex-column'>
                                                                        Rating: {product.rating.rate.toFixed(1)}
                                                                        <span>({product.rating.count} reviews)</span>
                                                                    </p>
                                                                </div>
                                                            )}

                                                        </div>
                                                        <p>{product.description}</p>
                                                    </div>
                                                </div>
                                            )
                                        })
                                    )}
                                </div>
                            </div>
                        </div>
                    );
                })}

                <span ref={dummy}></span>
            </div>
            <input
                id='text'
                onFocus={handleFocus}
                onChange={handleChange}
                onKeyDown={handleKeyPress}
                className="send-input"
                placeholder="Tell about your requirement..."
                type="text"
                name='text'
                value={state.text}
            />
            <div className="send" disabled={!state.text}>
                {
                    loader
                        ?
                        <ResponseLoader />
                        :
                        <>
                            <svg
                                onClick={handleSubmit}
                                className="send-icon"
                                id="Capa_1"
                                style={{
                                    enableBackground: 'new 0 0 512 512'
                                }}
                                version="1.1"
                                viewBox="0 0 512 512"
                                x="0px"
                                xmlSpace="preserve"
                                xmlns="http://www.w3.org/2000/svg"
                                xmlnsXlink="http://www.w3.org/1999/xlink"
                                y="0px"
                            >
                                <g>
                                    <g>
                                        <path
                                            d="M481.508,210.336L68.414,38.926c-17.403-7.222-37.064-4.045-51.309,8.287C2.86,59.547-3.098,78.551,1.558,96.808 L38.327,241h180.026c8.284,0,15.001,6.716,15.001,15.001c0,8.284-6.716,15.001-15.001,15.001H38.327L1.558,415.193 c-4.656,18.258,1.301,37.262,15.547,49.595c14.274,12.357,33.937,15.495,51.31,8.287l413.094-171.409 C500.317,293.862,512,276.364,512,256.001C512,235.638,500.317,218.139,481.508,210.336z"
                                            fill="#6B6C7B"
                                        />
                                    </g>
                                </g>
                            </svg>
                        </>
                }
            </div>
        </main>
    );
}
