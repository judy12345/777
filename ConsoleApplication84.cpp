#include "pch.h"
#include <iostream>

#include<stdio.h>
#include<stdlib.h>//调用system函数
#include<conio.h>
#include<string.h>
#define maxsize 600
#define INF 32767//两景点不可到距离长度
int visited[maxsize];//全局变量
int path[maxsize][maxsize];//经过景点
int shortest[maxsize][maxsize];//最短路径
typedef struct//定义对各个景点信息存储的结构体类型
{
	int top;//景点序号
	char info[maxsize];//景点名称
	char introduce[maxsize];//景点介绍
} data;//定义顶点类型
typedef struct node
{
	int adj;//相邻接的景点间的距离
} node;//定义边的类型
typedef struct
{
	data vertex[maxsize];//景点、顶点
	node arcs[maxsize][maxsize];//景点间距离
	int vexnum, arcnum;//景点数、边数
} adjmatrix;//定义图的类型

void Browser();/*校园地图*/
void PlaceList();/*已存景点阅览*/
void creatvisited(adjmatrix *g);/*访问标志数组初始化*/
void DFS(adjmatrix *g, int v);/*深度遍历*/
void search(adjmatrix *g);/*遍历*/
void vernumfile(adjmatrix *g);/*已存景点信息文本*/
void arcnumfile(adjmatrix *g);/*已存景点间路径文本*/
void readvernum(adjmatrix *g);/*读取景点信息*/
void readarcnum(adjmatrix *g);/*读取路径信息*/
void findvernum(adjmatrix *g);/*查询景点信息*/
void floyd(adjmatrix *g);/*弗洛伊德算法*/
void shortload(adjmatrix *g);/*最短路径*/
int meun();/*菜单栏*/




void Browser()
{
	printf(" 暨南大学校园平面图");
	printf("\n");
	printf("         南门                       ");
	printf("\n");
	printf("    //    ||      \\            \\  ");
	printf("\n");
	printf("   //     ||       \\            \\ ");
	printf("\n");
	printf("  //  恒大楼===惠全楼======操场");
	printf("\n");
	printf(" //       ||               ");
	printf("\n");
	printf("//        ||               ");
	printf("\n");
	printf("食堂  ||               ");
	printf("\n");
	printf("   \\     ||               ");
	printf("\n");
	printf("        学生宿舍            ");
	printf("\n");
	printf("          ||               ");
	printf("\n");
	printf("          ||               ");
	printf("\n");
	printf("      学生宿舍=====超市====学生宿舍           ");
	printf("\n");
	printf("             \\       \\        //            ");
	printf("\n");
	printf("               \\       \\     //             ");
	printf("\n");
	printf("                 \\       \\  //              ");
	printf("\n");
	printf("                         体育馆              ");
	printf("\n");
	printf("                           //                   ");
	printf("\n");
	printf("                          //                    ");
	printf("\n");
	printf("                        北门                ");
}

/*已存景点阅览*/
void PlaceList()
{
	system("color 00");
	printf("\t\t┏━━━━━━━━━━━━━━━━━━━━━━━━━┓\n");
	printf("\t\t┃已存文件景点一览表                                ┃\n");
	printf("\t\t┣━━━━━━━━━━━━┳━━━━━━━━━━━━┫\n");
	printf("\t\t┃1.恒大楼                ┃2惠全楼                 ┃\n");
	printf("\t\t┣━━━━━━━━━━━━╋━━━━━━━━━━━━┫\n");
	printf("\t\t┃3.食堂                  ┃4.体育馆                ┃\n");
	printf("\t\t┣━━━━━━━━━━━━╋━━━━━━━━━━━━┫\n");
	printf("\t\t┃5.超市                  ┃6.学生宿舍              ┃\n");
	printf("\t\t┣━━━━━━━━━━━━╋━━━━━━━━━━━━┫\n");
	printf("\t\t┃7.学生宿舍              ┃8.学生宿舍              ┃\n");
	printf("\t\t┣━━━━━━━━━━━━╋━━━━━━━━━━━━┫\n");
	printf("\t\t┃9.操场                  ┃10.南门                 ┃\n");
	printf("\t\t┗━━━━━━━━━━━━┻━━━━━━━━━━━━┛\n");
}

/*访问标志数组初始化*/
void creatvisited(adjmatrix *g)
{
	int i;
	for (i = 0; i < g->vexnum; i++)
		visited[i] = 0;
}
/*遍历*/
void search(adjmatrix *g)
{
	int i, n;
	creatvisited(g);
	for (i = 0; i < g->vexnum; i++)
		printf("%d\t%s\n", g->vertex[i].top, g->vertex[i].info);
	printf("请输入遍历的起点序号:(1-%d)\n", g->vexnum);
	scanf_s(" %d", &n);
	DFS(g, n - 1);
}

/*深度遍历*/
void DFS(adjmatrix *g, int v)
{
	int k;
	visited[v] = 1;//置已访问标记
	printf("景点序号:%d 名称:%s\n", g->vertex[v].top, g->vertex[v].info);
	for (k = 0; k < g->vexnum; k++)
		if (!visited[k] && g->arcs[v][k].adj != INF)
			DFS(g, k);
}
/*已存景点信息文本*/
void vernumfile(adjmatrix *g,int i)
{
	FILE *stream;
	errno_t err;
err = fopen_s(&stream,"1.txt","wt");
	
		fprintf(stream, "%d %s %s\n", g->vertex[i].top, g->vertex[i].info, g->vertex[i].introduce);
	fclose(stream);
}

/*已存景点间路径文本*/
/*void arcnumfile(adjmatrix *g)
{
	FILE *fp;
	int i, j;
	fp = fopen("arcnum.txt", "wt");
	for (i = 0; i < g->arcnum; i++)
		for (j = 0; j < g->arcnum; j++)
			if (g->arcs[i][j].adj != INF)
			{
				fprintf(fp, "%d %d %d\n", g->vertex[i].top, g->vertex[j].top, g->arcs[i][j].adj);
			}
	fclose(fp);
}*/
/*读取景点信息*/
void readvernum(adjmatrix *g)
{
	FILE *stream;
	errno_t err;
	int i = 0;
	err = fopen_s(&stream, "1.txt", "rt");
	if (stream == NULL) {
		printf("error");
		return;

	}

	fscanf_s(stream, " %d\n", &g->vexnum);
	char buffer[100];
	for (i = 0; i < g->vexnum; i++)
	{
		fscanf_s(stream," %d", &g->vertex[i].top);
		char ch = fgetc(stream);

		fgets(buffer,100,stream);
		*(strchr(buffer,'\n')) = '\0';
		strcpy_s(g->vertex[i].info,strlen(buffer) + 1,buffer);
		fgets(buffer,200,stream);
		*(strchr(buffer,'\n')) = '\0';
		strcpy_s(g->vertex[i].introduce,strlen(buffer) + 1,buffer);
	}
	printf("景点个数：%d\n", g->vexnum);
	for (int i = 0; i < g->vexnum; i++) {
		
		printf("景点序号: %d 名称: %s\n", g->vertex[i].top, g->vertex[i].info);
		printf("景点信息: %s\n", g->vertex[i].introduce);
		printf("\n");
	}


	fclose(stream);
}
/*读取路径信息*/
 void readarcnum(adjmatrix *g) {
	int i, j;
	for (i = 0; i < g->vexnum; ++i) {
		for (j = 0; j < g->vexnum; j++) {
			g->arcs[i][j].adj = INF;
		}
	}
	g->arcs[1][2].adj = g->arcs[2][1].adj = 50;
	g->arcs[1][3].adj = g->arcs[3][1].adj = 60;
	g->arcs[2][3].adj = g->arcs[3][2].adj = 30;
	g->arcs[3][4].adj = g->arcs[4][3].adj = 10;
	g->arcs[2][5].adj = g->arcs[5][2].adj = 20;
	g->arcs[5][6].adj = g->arcs[6][5].adj = 40;
	g->arcs[6][7].adj = g->arcs[7][6].adj = 30;
	g->arcs[7][8].adj = g->arcs[8][7].adj = 20;
	g->arcs[8][9].adj = g->arcs[9][8].adj = 10;
	g->arcs[10][9].adj = g->arcs[9][10].adj = 20;
}

/*{
	errno_t err;
	FILE *stream;
	int i = 0, j = 0, k = 0;
	err = fopen_s(&stream, "D://2.txt", "rt");
	for (i = 0; i < g->vexnum; i++) {
		for (j = 0; j < g->vexnum; j++) {
			g->arcs[i][j].adj = INF;

			while (fscanf_s(stream, "%d%d%d", &i, &j, &k) != EOF)
			{
				g->arcs[i][j].adj = k;
			}
		}
	}
	fclose(stream);
}*/
/*  读取景点信息*/
void findvernum(adjmatrix *g)
{
	int i, n;
	char choice;
	for (i = 0; i < g->vexnum; i++)
		printf("%d\t%s\n", g->vertex[i].top, g->vertex[i].info);
	do
	{
		printf("请输入要查询的景点序号(1-%d):\n", g->vexnum);
		scanf_s(" %d", &n);
		printf("景点名称:%s\n", g->vertex[n - 1].info);
		printf("景点信息:%s\n", g->vertex[n - 1].introduce);
		printf("\n");
		printf("是否继续查询:(y/n):\n");
		_flushall();
		scanf_s(" %c", &choice, 1);
	} while (choice == 'Y' || choice == 'y');
}
int Addnewsight(adjmatrix *g) {
	int i;
	char sight[100], decription[1000]; int length;
	if (g->vexnum <= maxsize)
	{
		printf("请输入新景点的名称：");
		scanf_s(" %s", &sight,100);
		printf("请输入景点的相关信息：");
		scanf_s("%s", &decription, 200);
		strcpy_s()
		for (i = 0; i < g->vexnum; i++) {
			printf("请输入此景点到第%d个景点的距离", i);
			scanf_s("%d", &g->arcs[g->vexnum][i].adj);
			g->arcnum++;
			g->vexnum++;
			g->arcs[i][g->vexnum].adj = g->arcs[g->vexnum][i].adj;
			vernumfile(g, g->vexnum);
		}
	}return 0;
}
/*弗洛伊德算法*/
void floyd(adjmatrix *g)
{
	int i, j, k;
	for (i = 0; i < g->vexnum; i++) {
		for (j = 0; j < g->vexnum; j++) {
			shortest[i][j] = 0;
		}
	}
	for (i = 0; i < g->vexnum; i++) {
		for (j = 0; j < g->vexnum; j++)
		{
			shortest[i][j] = g->arcs[i][j].adj;
			path[i][j] = 0;
		}
	}
	for (k = 0; k < g->vexnum; k++)
	{
		for (i = 0; i < g->vexnum; i++) {
			for (j = 0; j < g->vexnum; j++) {


				if (shortest[i][j] > (shortest[i][k] + shortest[k][j]))
				{
					shortest[i][j] = shortest[i][k] + shortest[k][j];
					path[i][j] = k;
					path[j][i] = k;
				}
			}
		}
	}
}
/*最短路径*/
void shortload(adjmatrix *g)
{
	int i, j, a, b;
	PlaceList();
	floyd(g);
	printf("请输入起始景点和终止景点(1-%d):\n", g->vexnum);
	scanf_s(" %d %d", &i, &j);
	a = i;
	b = j;
	i = i - 1;
	j = j - 1;
	if (i < j)
	{
		printf("%d", b);
		while (path[i][j] != 0)
		{
			printf("<-%d", path[i][j] + 1);
			if (i < j)
				j = path[i][j];
			else
				i = path[j][i];
		}
		printf("<-%d", a);
		printf("\n\n");
		printf("%d->%d 距离是:%d米\n\n", a, b, shortest[a - 1][b - 1]);
	}
	else
	{
		printf("%d", a);
		while (path[i][j] != 0)
		{
			printf("<-%d", path[i][j] + 1);
			if (i < j)
				j = path[i][j];
			else
				i = path[j][i];
		}
		printf("<-%d", b);
		printf("\n\n");
		printf("%d->%d 最短距离是:%d米\n\n", a, b, shortest[a - 1][b - 1]);
	}
}

/*菜单栏*/
int meun()
{
	char choice;
	adjmatrix *g;
	g = (adjmatrix *)malloc(sizeof(adjmatrix));//创建头结点
	system("color 00");
	while (1)
	{
		printf("\n");
		printf("\t\t************************************************\n");
		printf("\t\t***************校园景点导航系统*****************\n");
		printf("\t\t*****************欢迎您的使用*******************\n");
		printf("\t\t************************************************\n");
		printf("\t\t**\t 1: 读取文件信息**\n");
		printf("\t\t**\t 2: 遍历景点信息**\n");
		printf("\t\t**\t 3: 查询景点信息**\n");
		printf("\t\t**\t 4: 查询最短路径**\n");
		printf("\t\t**\t 5: 查看景点地图**\n");
		printf("\t\t**\t 0: 退出查询系统**\n");
		printf("\t\t************************************************\n");
		printf("\t\t************************************************\n");
		printf("\n");
		printf("请选择需要使用的功能序号:");
		choice = getchar();
		switch (choice)
		{
		case '1':
		{
			readvernum(g);
			readarcnum(g);
			break;
		}
		case '2':
		{
			search(g);
			break;
		}
		case '3':
		{
			findvernum(g);
			break;
		}
		case '4':
		{
			shortload(g);
			break;
		}
		case '5':
		{
			Browser();
			break;
		}
		case '6':
		{ Addnewsight(g);
		break;
		}
		case '0':
		{
			printf("谢谢使用,再见!\n");
			exit(0);
		}
		}

		printf("请按任意键继续.....");
		_getch();
		_flushall();
		system("cls");

	}
	free(g);
	g =NULL;
}







		/*主函数*/
int main()
{
	printf("2018050058 网安韩雨薇");
	meun();
	return 0;
}


// ConsoleApplication84.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//




// 运行程序: Ctrl + F5 或调试 >“开始执行(不调试)”菜单
// 调试程序: F5 或调试 >“开始调试”菜单

// 入门提示: 
//   1. 使用解决方案资源管理器窗口添加/管理文件
//   2. 使用团队资源管理器窗口连接到源代码管理
//   3. 使用输出窗口查看生成输出和其他消息
//   4. 使用错误列表窗口查看错误
//   5. 转到“项目”>“添加新项”以创建新的代码文件，或转到“项目”>“添加现有项”以将现有代码文件添加到项目
//   6. 将来，若要再次打开此项目，请转到“文件”>“打开”>“项目”并选择 .sln 文件
