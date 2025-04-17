import {useState, useEffect, useRef,} from 'react';
import {Tabs} from 'antd';
import {useLocation, useNavigate, useOutlet} from 'react-router-dom';
import {MenuItems} from './menu_items.jsx'

const AdminHomeTabs = () => {
    const [activeKey, setActiveKey] = useState('');
    const [items, setItems] = useState([]);
    const newTabIndex = useRef(0);
    const location = useLocation();
    const navigate = useNavigate();
    const tabCache = useRef({});
    const outlet = useOutlet()


function findMatchingMenuItem(menu, currentPath) {
    for (let i = 0; i < menu.length; i++) {
        const item = menu[i];
        if (item.path === currentPath) {
            return item.cn;
        }

        if (item.children) {
            let found = null;
            if (Array.isArray(item.children)) {
                found = findMatchingMenuItem(item.children, currentPath);
            } else if (typeof item.children === "object" && item.children !== null) {
                found = findMatchingMenuItem(Object.values(item.children), currentPath);
            }
            if (found) return item.cn + "/" + found;
        }
    }

    return null;
}


    useEffect(() => {
        let path = location.pathname;
        if (path === "/") {
            return
        }

        path = findMatchingMenuItem(MenuItems, path)

        if (!items.find(item => item.key === path)) {
            addTab(path, path);
        }
        setActiveKey(path);
    }, [location]);

    const onChange = (newActiveKey) => {
        for (let i = 0; i < MenuItems.length; i++) {
            if (MenuItems[i].cn == newActiveKey) {
                newActiveKey = MenuItems[i].path
            }
        }
        setActiveKey(newActiveKey);
        navigate(newActiveKey);
    };

    const addTab = (path, label) => {
        const newActiveKey = path;
        const newPanes = [...items];
        newPanes.push({label, key: newActiveKey});
        setItems(newPanes);
        setActiveKey(newActiveKey);
        // console.log(newActiveKey)
        if (!tabCache.current[newActiveKey]) {
            tabCache.current[newActiveKey] = outlet;
        }
    };

    const remove = (targetKey) => {
        let newActiveKey = activeKey;
        let lastIndex = -1;
        items.forEach((item, i) => {
            if (item.key === targetKey) {
                lastIndex = i - 1;
            }
        });
        const newPanes = items.filter((item) => item.key !== targetKey);
        if (newPanes.length && newActiveKey === targetKey) {
            if (lastIndex >= 0) {
                newActiveKey = newPanes[lastIndex].key;
            } else {
                newActiveKey = newPanes[0].key;
            }
        }
        setItems(newPanes);
        setActiveKey(newActiveKey);
    };
    const onEdit = (targetKey, action) => {
        if (action === 'add') {
            // add();
        } else {
            remove(targetKey);
        }
    };

    return (
        <Tabs
            type="editable-card"
            onChange={onChange}
            activeKey={activeKey}
            onEdit={onEdit}
            hideAdd={true}
            items={items.map(item => ({
                ...item,
                className: 'custom-tab-class',
                // Use tabCache to render the content of each tab
                children: tabCache.current[item.key] || <div>{item.label}</div>
            }))}
        />
    );
};

export default AdminHomeTabs;
