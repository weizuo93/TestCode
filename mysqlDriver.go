// 1.下载Go安装包（https://go.dev/dl/），并在本地解压。
// 2.下载Go程序开发环境（https://www.jetbrains.com/go/），并在本地解压。
// 3.在~/.bashrc文件中配置GO程序相关的环境变量PATH和GOROOT：
//   `export PATH=/home/mi/program/go/bin:$PATH`
//   `export GOROOT=/home/mi/program/go`
//   `export PATH=/home/mi/program/GoLand-2022.1.3/bin:$PATH`
// 4.在Goland软件中配置”Flie->Settings->GO->GOPATH“下配置GOPATH为工程目录：
//   GOPATH: `/home/mi/Project/Golang/MysqlConnection`
// 5.在GOPATH所在目录下执行`go get -u github.com/go-sql-driver/mysql`，下载go-sql-driver

package main

import (
	"database/sql"
	"errors"
	"fmt"
	_ "github.com/go-sql-driver/mysql"
	"log"
	"strings"
)

const (
	userName = "xxx"
	password = "xxx"
	ip       = "xxx"
	port     = "xxx"
	dbName   = "xxx"
)

var DB *sql.DB

func InitDB() {
	//构建连接："用户名:密码@tcp(IP:端口)/数据库?charset=utf8"
	path := strings.Join([]string{userName, ":", password, "@tcp(", ip, ":", port, ")/", dbName, "?charset=utf8"}, "")

	//打开数据库,前者是驱动名，所以要导入： _ "github.com/go-sql-driver/mysql"
	DB, _ = sql.Open("mysql", path)
	//设置数据库最大连接数
	DB.SetConnMaxLifetime(100)
	//设置上数据库最大闲置连接数
	DB.SetMaxIdleConns(10)
	//验证连接
	if err := DB.Ping(); err != nil {
		fmt.Println("opon database fail")
		return
	}
	fmt.Println("connnect success")
}

func queryDB() {
	var eventDay, siteId, cityCode, useName, pv string
	rows, e := DB.Query("select * from table_test")
	if e == nil {
		errors.New("query incur error")
	}
	fmt.Printf("event_day, siteid, citycode, userName, pv\n")
	for rows.Next() {
		e := rows.Scan(&eventDay, &siteId, &cityCode, &useName, &pv)
		if e != nil {
		}
		fmt.Printf("%s, %s, %s, %s, %s\n", eventDay, siteId, cityCode, useName, pv)
	}
	rows.Close()
}

func ddlDB() {
	stmt := `
		CREATE TABLE IF NOT EXISTS table_test_1
		(
			eventDay DATE,
			siteId INT DEFAULT '10',
			cityCode SMALLINT,
			userName VARCHAR(32) DEFAULT '',
			pv BIGINT DEFAULT '0'
		)
		DUPLICATE KEY(eventDay, siteId, cityCode, userName)
		DISTRIBUTED BY HASH(siteId) BUCKETS 1
		PROPERTIES("replication_num" = "3")
		`
	_, err := DB.Exec(stmt)
	if err != nil {
		log.Fatalln(err)
	}
	fmt.Printf("succeed to exec:\n %s", stmt)
}

func main() {
	InitDB()
	queryDB()
	ddlDB()
}
