<?php
/**
 * @link      http://github.com/zendframework/ZendSkeletonApplication for the canonical source repository
 * @copyright Copyright (c) 2005-2016 Zend Technologies USA Inc. (http://www.zend.com)
 * @license   http://framework.zend.com/license/new-bsd New BSD License
 */

namespace Application;

use Zend\ModuleManager\Feature\ConfigProviderInterface;
use Zend\Db\Adapter\AdapterInterface;
use Zend\Db\ResultSet\ResultSet;
use Zend\Db\TableGateway\TableGateway;

class Module implements ConfigProviderInterface 
{
    
    const VERSION = '0.1';
    
    public function getConfig() {
        return include __DIR__ . '/../config/module.config.php';
    }
    
    public function getServiceConfig() {
        
        return [
            
            'factories' => [
                
                Model\AgentTable::class => function($container) {
                    $tableGateway = $container->get(Model\AgentTableGateway::class);
                    return new Model\AgentTable($tableGateway);
                },
                        
                Model\AgentTableGateway::class => function($container) {
                    
                    $dbAdapter = $container->get(AdapterInterface::class);
                    $resultSetPrototype = new ResultSet();
                    $resultSetPrototype->setArrayObjectPrototype(new Model\Album());
                    return new TableGateway('agents', $dbAdapter, null, $resultSetPrototype);
                    
                },
                
            ],
            
        ];
        
    }
    
    public function getControllerConfig() {
        
        return [
            
            'factories' => [
                
                Controller\AgentController::class => function($container) {
                    return new Controller\AgentController($container->get(Model\AgentTable::class));
                },
                
            ],
            
        ];
        
    }

}