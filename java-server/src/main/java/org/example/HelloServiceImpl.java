package org.example;

public class HelloServiceImpl implements HelloService.Iface {

    @Override
    public String helloFunc(String para) {
        System.out.println(para);
        return "(Returned from Java Server) Original message: " + para;
    }
}