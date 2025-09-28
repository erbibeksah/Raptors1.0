namespace Omni.Migrations.Globals.Setup;

/// <summary>
/// Create Migration for User Table
/// </summary>
/// <remarks>
/// ⚠️ This migration no must be in this format {yy-mm-dd-hour-minute} is intended to use {two-digit}**.
/// </remarks>
[Migration(202609272116)]
public  class M001_Create_User_Table : Migration
{
    public override void Up()
    {
        this.Create.Table("t_ROLEMST")
                .WithColumn("ID").AsGuid().PrimaryKey().NotNullable()
                .WithColumn("ROLENAME").AsString(50).NotNullable()
                .WithColumn("ISADMIN").AsBoolean().NotNullable()
                .WithColumn("ISSUPERADMIN").AsBoolean().NotNullable()
                .WithColumn("ISACTIVEROLE").AsBoolean().NotNullable()
                .WithColumn("CREATEDAT").AsDateTime().WithDefault(SystemMethods.CurrentUTCDateTime)
                .WithColumn("UPDATEDAT").AsDateTime().Nullable()
                .WithColumn("MODIFIEDBY").AsString(30).Nullable();

        this.Create.Table("t_USERMST")
                 .WithColumn("ID").AsGuid().PrimaryKey().NotNullable()
                 .WithColumn("ROLEID").AsGuid().NotNullable()
                 .WithColumn("USERNAME").AsString(50).NotNullable()
                 .WithColumn("USERPASSWORD").AsString(int.MaxValue).Nullable()
                 .WithColumn("FIRSTNAME").AsString(50).NotNullable()
                 .WithColumn("MIDDLENAME").AsString(50).Nullable()
                 .WithColumn("LASTNAME").AsString(50).NotNullable()
                 .WithColumn("PERSONALEMAIL").AsString(50).Nullable()
                 .WithColumn("COMPANYEMAIL").AsString(50).Nullable()
                 .WithColumn("PERSONALMOBILENO").AsString(50).Nullable()
                 .WithColumn("COMPANYMOBILENO").AsString(50).Nullable()
                 .WithColumn("ISACTIVE").AsBoolean().NotNullable()
                 .WithColumn("USERIPADDRESS").AsString(30).Nullable()
                 .WithColumn("CREATEDAT").AsDateTime().WithDefault(SystemMethods.CurrentUTCDateTime)
                 .WithColumn("UPDATEDAT").AsDateTime().Nullable()
                 .WithColumn("MODIFIEDBY").AsString(30).Nullable();

        // Add foreign key
        this.Create.ForeignKey("FK_USERMST_ROLEID")
            .FromTable("t_USERMST").ForeignColumn("ROLEID")
            .ToTable("t_ROLEMST").PrimaryColumn("ID");

        var adminRoleId = Guid.CreateVersion7();
        var superAdminRoleId = Guid.CreateVersion7();

        this.Insert.IntoTable("t_ROLEMST").Row(new
        {
            ID = adminRoleId,
            ROLENAME = "Admin",
            ISADMIN = true,
            ISSUPERADMIN = false,
            ISACTIVEROLE = true,
            CREATEDAT = DateTime.UtcNow
        });

        this.Insert.IntoTable("t_ROLEMST").Row(new
        {
            ID = superAdminRoleId,
            ROLENAME = "SuperAdmin",
            ISADMIN = true,
            ISSUPERADMIN = true,
            ISACTIVEROLE = true,
            CREATEDAT = DateTime.UtcNow
        });

        this.Insert.IntoTable("t_USERMST").Row(new
        {
            ID = Guid.CreateVersion7(),
            ROLEID = adminRoleId,
            USERNAME = "admin",
            USERPASSWORD = "admin@123",
            FIRSTNAME = "Admin",
            LASTNAME = "Admin",
            ISACTIVE = true,
            CREATEDAT = DateTime.UtcNow
        });

        this.Insert.IntoTable("t_USERMST").Row(new
        {
            ID = Guid.CreateVersion7(),
            ROLEID = superAdminRoleId,
            USERNAME = "superadmin",
            USERPASSWORD = "superadmin@123",
            FIRSTNAME = "SuperAdmin",
            LASTNAME = "SuperAdmin",
            ISACTIVE = true,
            CREATEDAT = DateTime.UtcNow
        });

        this.Execute.EmbeddedScript("USR_GetByUserName.sql");
    }

    /// <summary>
    /// Rollback migration for the 't_userMst' table.
    /// </summary>
    /// <remarks>
    /// ⚠️ This rollback method is intended for **emergency use only**.
    /// Use with caution in production environments.
    ///
    /// Calling this will drop the 't_userMst' table and delete all user records.
    ///
    /// Use programmatically via:
    /// <code>runner.Rollback(1);</code>
    /// </remarks>
    public override void Down()
    {
        // not needed as of now
        // Delete.Table("tbl_userMst");
    }

}