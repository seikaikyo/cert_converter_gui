#!/bin/bash

# GitLab 和 GitHub 倉庫檢查與同步腳本

# 顏色代碼，使輸出更易讀
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # 無顏色

# 檢查當前目錄是否為 git 倉庫
if [ ! -d ".git" ]; then
    echo -e "${RED}錯誤：當前目錄不是 Git 倉庫。${NC}"
    exit 1
fi

# 檢查 Git 遠端配置
echo -e "${YELLOW}檢查 Git 遠端...${NC}"
git remote -v

# 識別 GitLab 遠端
if git remote -v | grep -q "gitlab"; then
    GITLAB_REMOTE=$(git remote -v | grep "gitlab" | grep "(push)" | head -n1 | awk '{print $1}')
    echo -e "${GREEN}✓ 找到 GitLab 遠端：${GITLAB_REMOTE}${NC}"
elif git remote -v | grep -q "origin"; then
    GITLAB_REMOTE="origin"
    echo -e "${YELLOW}? 假設 'origin' 是您的 GitLab 遠端${NC}"
else
    echo -e "${RED}✗ 未找到 GitLab 遠端${NC}"
    echo -e "${YELLOW}是否要添加 GitLab 遠端？(y/n)${NC}"
    read add_gitlab
    if [ "$add_gitlab" = "y" ] || [ "$add_gitlab" = "Y" ]; then
        echo -e "${YELLOW}請輸入您的 GitLab 倉庫 URL：${NC}"
        read gitlab_url
        git remote add gitlab "$gitlab_url"
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✓ GitLab 遠端添加成功${NC}"
            GITLAB_REMOTE="gitlab"
        else
            echo -e "${RED}✗ 添加 GitLab 遠端失敗${NC}"
        fi
    fi
fi

# 識別 GitHub 遠端
if git remote -v | grep -q "github"; then
    GITHUB_REMOTE=$(git remote -v | grep "github" | grep "(push)" | head -n1 | awk '{print $1}')
    echo -e "${GREEN}✓ 找到 GitHub 遠端：${GITHUB_REMOTE}${NC}"
else
    echo -e "${RED}✗ 未找到 GitHub 遠端${NC}"
    echo -e "${YELLOW}是否要添加 GitHub 遠端？(y/n)${NC}"
    read add_github
    if [ "$add_github" = "y" ] || [ "$add_github" = "Y" ]; then
        echo -e "${YELLOW}請輸入您的 GitHub 倉庫 URL：${NC}"
        read github_url
        git remote add github "$github_url"
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✓ GitHub 遠端添加成功${NC}"
            GITHUB_REMOTE="github"
        else
            echo -e "${RED}✗ 添加 GitHub 遠端失敗${NC}"
        fi
    fi
fi

# 獲取當前分支
CURRENT_BRANCH=$(git branch --show-current)
echo -e "${YELLOW}當前分支: ${CURRENT_BRANCH}${NC}"

# 如果兩個遠端都配置好了
if [ ! -z "$GITLAB_REMOTE" ] && [ ! -z "$GITHUB_REMOTE" ]; then
    # 檢查是否要設置 'all' 遠端（用於一次性推送到兩個倉庫）
    if ! git remote -v | grep -q "all"; then
        echo -e "${YELLOW}是否要設置一個 'all' 遠端以同時推送到兩個倉庫？(y/n)${NC}"
        read setup_all
        
        if [ "$setup_all" = "y" ] || [ "$setup_all" = "Y" ]; then
            GITLAB_URL=$(git remote get-url --push "$GITLAB_REMOTE")
            GITHUB_URL=$(git remote get-url --push "$GITHUB_REMOTE")
            
            git remote add all "$GITLAB_URL"
            git remote set-url --add --push all "$GITLAB_URL"
            git remote set-url --add --push all "$GITHUB_URL"
            
            if [ $? -eq 0 ]; then
                echo -e "${GREEN}✓ 成功設置 'all' 遠端${NC}"
                echo -e "${YELLOW}現在您可以使用以下命令推送到兩個倉庫：${GREEN}git push all${NC}"
            else
                echo -e "${RED}✗ 設置 'all' 遠端失敗${NC}"
            fi
        fi
    else
        echo -e "${GREEN}✓ 'all' 遠端已配置${NC}"
    fi
    
    # 詢問是否要立即推送
    echo -e "${YELLOW}是否現在要推送到兩個倉庫？(y/n)${NC}"
    read push_now
    
    if [ "$push_now" = "y" ] || [ "$push_now" = "Y" ]; then
        if git remote -v | grep -q "all"; then
            echo -e "${YELLOW}通過 'all' 遠端推送到兩個倉庫...${NC}"
            git push all "$CURRENT_BRANCH"
            
            if [ $? -eq 0 ]; then
                echo -e "${GREEN}✓ 成功推送到兩個倉庫${NC}"
            else
                echo -e "${RED}✗ 推送到兩個倉庫失敗${NC}"
                
                # 嘗試單獨推送
                echo -e "${YELLOW}嘗試單獨推送...${NC}"
                
                echo -e "${YELLOW}推送到 GitLab (${GITLAB_REMOTE})...${NC}"
                git push "$GITLAB_REMOTE" "$CURRENT_BRANCH"
                
                echo -e "${YELLOW}推送到 GitHub (${GITHUB_REMOTE})...${NC}"
                git push "$GITHUB_REMOTE" "$CURRENT_BRANCH"
            fi
        else
            # 單獨推送到每個倉庫
            if [ ! -z "$GITLAB_REMOTE" ]; then
                echo -e "${YELLOW}推送到 GitLab (${GITLAB_REMOTE})...${NC}"
                git push "$GITLAB_REMOTE" "$CURRENT_BRANCH"
                if [ $? -eq 0 ]; then
                    echo -e "${GREEN}✓ 成功推送到 GitLab${NC}"
                else
                    echo -e "${RED}✗ 推送到 GitLab 失敗${NC}"
                fi
            fi
            
            if [ ! -z "$GITHUB_REMOTE" ]; then
                echo -e "${YELLOW}推送到 GitHub (${GITHUB_REMOTE})...${NC}"
                git push "$GITHUB_REMOTE" "$CURRENT_BRANCH"
                if [ $? -eq 0 ]; then
                    echo -e "${GREEN}✓ 成功推送到 GitHub${NC}"
                else
                    echo -e "${RED}✗ 推送到 GitHub 失敗${NC}"
                fi
            fi
        fi
    fi
fi

echo -e "${GREEN}腳本執行完成。${NC}"