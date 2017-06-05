from troposphere import GetAtt, Output, Ref
from troposphere.ec2 import Tag
from troposphere.rds import DBInstance, DBSubnetGroup

from stacker.blueprints.base import Blueprint


class Database(Blueprint):

    VARIABLES = {
        "SubnetIds": {
            "type": list,
            "description": "List of DB subnet ids"
        },
        "SecurityGroups": {
            "type": list,
            "description": "List of DB security groups"
        },
        "Name": {
            "type": str,
            "description": "DB name"
        },
        "Username": {
            "type": str,
            "description": "DB user"
        },
        "Password": {
            "type": str,
            "description": "DB password"
        },
        "InstanceClass": {
            "type": str,
            "description": "DB class"
        },
        "Engine": {
            "type": str,
            "description": "DB engine"
        },
        "EngineVersion": {
            "type": str,
            "description": "DB engine version"
        },
        "Size": {
            "type": int,
            "description": "DB size (Gb)"
        },
        "StorageEncryption": {
            "type": bool,
            "description": "Enable encryption at rest"
        },
        "MultiAz": {
            "type": bool,
            "description": "Enable multi az"
        },
        "Tags": {
            "type": dict,
            "description": "Tags to apply to DB"
        }
    }

    def create_db_subnet_group(self):
        variables = self.get_variables()
        self.subnet_group = self.template.add_resource(DBSubnetGroup(
            "SubnetGroup",
            DBSubnetGroupDescription="Subnets available for DB instances",
            SubnetIds=variables["SubnetIds"],
        ))

    def create_db(self):
        variables = self.get_variables()

        self.template.add_resource(DBInstance(
            "DB",
            DBName=variables["Name"],
            AllocatedStorage=variables["Size"],
            DBInstanceClass=variables["InstanceClass"],
            Engine=variables["Engine"],
            EngineVersion=variables["EngineVersion"],
            MasterUsername=variables["Username"],
            MasterUserPassword=variables["Password"],
            DBSubnetGroupName=Ref(self.subnet_group),
            VPCSecurityGroups=variables["SecurityGroups"],
            MultiAZ=variables["MultiAz"],
            StorageType="gp2",
            StorageEncrypted=variables["StorageEncryption"],
            Tags=[
                Tag(key, value)
                for key, value in variables["Tags"].iteritems()
            ]
        ))

        self.template.add_output(Output(
            "Address",
            Description="Database address",
            Value=GetAtt("DB", "Endpoint.Address")
        ))

        self.template.add_output(Output(
            "Port",
            Description="Database port",
            Value=GetAtt("DB", "Endpoint.Port")
        ))

    def create_template(self):
        self.create_db_subnet_group()
        self.create_db()
